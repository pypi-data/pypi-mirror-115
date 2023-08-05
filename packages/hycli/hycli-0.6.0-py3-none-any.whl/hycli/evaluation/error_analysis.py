from pathlib import Path
import typing
from sqlite3 import Error

import tempfile
from fpdf import FPDF
from PIL import Image, UnidentifiedImageError
import pdf2image

from hycli.evaluation.evaluation import Database, col_entity_error, col_entity_improvement


def error_analysis(
    job_id, num_docs=20, num_vendors=10, db_dir=None
) -> typing.Type[typing.Tuple[typing.List, typing.List]]:
    """Analyze the errors on document level based on a previous evaluation job.

    Args:
        job_id (str): The ID of the previous evaluation job.
        num_docs (int): Specify how many images you would analyze.
        num_vendors (int): Specify how many vendors you would analyze. This field only works if `vendor_field` is
            specified in the evaluation job.
        db_dir (Path): The directory of the database file.

    """

    db = Database(db_dir=db_dir)
    if not db.table_exist(f"merged_comparison_{job_id}"):
        raise Exception(
            f"The merged_comparison_{job_id} table does not exist in {db_dir}/pythonsqlite.db. \n"
            f"Please check if the job_id and db_dir are correct. "
        )

    cur = db.conn.cursor()
    cur.execute(f"""SELECT DISTINCT entity FROM entity WHERE job_id = '{job_id}';""")
    rows = cur.fetchall()
    entities = [entity for (entity,) in rows]
    cols_entity_error = [col_entity_error(entity, "m2") for entity in entities]
    cols = [
        f"""{entity}_gt,
        {entity}_m1,
        {entity}_m2,
        {col_entity_error(entity, 'm1')},
        {col_entity_error(entity, 'm2')},
        {col_entity_improvement(entity)} """
        for entity in entities
    ]
    cur.execute(f"""SELECT DISTINCT vendor FROM vendor WHERE job_id = '{job_id}'; """)
    vendors = cur.fetchall()
    if len(vendors) == 0:
        query = f"""
        SELECT file_name,
            '' AS vendor,
            {", ".join(cols)}
        FROM merged_comparison_{job_id}
        ORDER BY number_of_errors_m2 DESC
        LIMIT {num_docs};
        """
    else:

        query = f"""
        SELECT file_name,
            vendor,
            {", ".join(cols)}
        FROM merged_comparison_{job_id}
        WHERE vendor IN (
            SELECT vendor
            FROM vendor
            WHERE job_id = '{job_id}'
              AND model_id = 2
              AND number_of_errors > 0
            ORDER BY no_touch_rate
            LIMIT {num_vendors})
          AND ({" + ".join(cols_entity_error)}) > 0
        LIMIT {num_docs};
        """
    try:
        cur.execute(query)
    except Error as e:
        print(query)
        raise e
    query_results = cur.fetchall()

    return entities, query_results


def create_error_analysis_report(entities, query_results, docs_dir: Path):
    pdf = FPDF("L")
    cell_width = 28
    cell_height = 10
    for row in query_results:
        file_name = row[0]
        vendor = row[1]
        pdf.add_page()
        pdf.set_xy(x=pdf.w * 0.20, y=3)
        pdf.set_font("Arial", "", 10)
        pdf.cell(cell_width, cell_height, file_name, ln=2)
        image_file_path = docs_dir / file_name
        # Add image to pdf
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            try:
                img = Image.open(image_file_path)[0]
            except UnidentifiedImageError:
                img = pdf2image.convert_from_path(image_file_path)[0]
            img.save(fp.name)
            pdf.image(fp.name, w=pdf.w / 2, h=pdf.h * 0.9, x=3, y=15)
        # Add extraction data to pdf
        # ln parameter: 0=to the right, 1=to the beginning of the next line, 2=below
        pdf.set_xy(x=pdf.w * 0.52, y=pdf.get_y())
        pdf.cell(
            cell_width,
            cell_height,
            f"Vendor: {vendor.encode('latin-1', 'replace').decode('latin-1')}",
            border=0,
            ln=2,
        )
        pdf.cell(cell_width * 1.5, cell_height, "Entity", border=1, ln=0)
        pdf.cell(cell_width, cell_height, "GT", border=1, ln=0)
        pdf.cell(cell_width, cell_height, "M1", border=1, ln=0)
        pdf.cell(cell_width, cell_height, "M2", border=1, ln=0)
        pdf.cell(cell_width, cell_height, "Improv.", border=1, ln=1)
        pdf.set_xy(x=pdf.w * 0.52, y=pdf.get_y())

        idx = 0
        for entity in entities:
            (
                entity_gt,
                entity_m1,
                entity_m2,
                entity_error_m1,
                entity_error_m2,
                entity_improve,
            ) = row[2 + idx * 6 : 2 + (idx + 1) * 6]
            if entity_error_m2 == 1:
                pdf.cell(cell_width * 1.5, cell_height, entity.replace("_", " "), border=1, ln=0)
                pdf.cell(
                    cell_width,
                    cell_height,
                    str(entity_gt).encode("latin-1", "replace").decode("latin-1"),
                    border=1,
                    ln=0,
                )
                pdf.cell(
                    cell_width,
                    cell_height,
                    str(entity_m1).encode("latin-1", "replace").decode("latin-1"),
                    border=1,
                    ln=0,
                )
                pdf.cell(
                    cell_width,
                    cell_height,
                    str(entity_m2).encode("latin-1", "replace").decode("latin-1"),
                    border=1,
                    ln=0,
                )
                pdf.cell(cell_width, cell_height, str(entity_improve), border=1, ln=1)
                pdf.set_xy(x=pdf.w * 0.52, y=pdf.get_y())
            idx += 1
    return pdf
