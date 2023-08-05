import csv
import json
from pathlib import Path

import click
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from hycli.evaluation.evaluation import Evaluation, Granularity
from hycli.evaluation.error_analysis import error_analysis as analysis, create_error_analysis_report
from hycli.commands.context_default import CONTEXT_SETTINGS


def job_id_required_options(ctx, param, value):
    if value is None:
        if not ctx.obj.get("ground_truth_file"):
            set_option_as_required(ctx, "ground_truth_file")
        if not ctx.obj.get("model_1_file"):
            set_option_as_required(ctx, "model_1_file")
        if not ctx.obj.get("model_2_file"):
            set_option_as_required(ctx, "model_2_file")
    return value


def set_option_as_required(ctx, name):
    for p in ctx.command.params:
        if isinstance(p, click.Option) and p.name == name:
            p.required = True


def error_analysis_args(ctx, param, value):
    if value:
        if not ctx.obj.get("doc_dir"):
            set_option_as_required(ctx, "doc_dir")
    return value


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--job-id",
    "-j",
    default=None,
    help='Definition: The ID for the evaluation in format "%Y%m%d_%H%M%S".\n'
    "Instruction: Only enter job_id if you want to get a report from a previous job.\n"
    "Leave it empty if running a report for the first time.",
    callback=job_id_required_options,
)
@click.option(
    "--ground-truth-file",
    "-gt",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the ground truth file.\n"
    "Instruction: Only enter ground_truth_file if you want to create a new report.\n"
    "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--model-1-file",
    "-m1",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the model 1 extractions.\n"
    "Instruction: Only enter model_1_file if you want to create a new report.\n"
    "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--model-2-file",
    "-m2",
    default=None,
    type=click.Path(exists=True),
    help="Definition: Path to the model 2 extractions.\n"
    "Instruction: Only enter model_2_file if you want to create a new report.\n"
    "Leave it empty if you want to get a report from a previous job.",
)
@click.option(
    "--entities",
    "-e",
    default=None,
    help="Definition: Entity that will be used for model evaluation.\n"
    "Accepts multiple values",
    multiple=True,
)
@click.option(
    "--vendor-field",
    "-v",
    default=None,
    help="Definition: Column name for the vendor id.\n"
    "Instruction: Only enter vendor_field if you want to create a vendor report.\n"
    "Leave it empty if you are not interested in a vendor performance report.",
)
@click.option(
    "--report-dir",
    "-r",
    default="report",
    type=click.Path(),
    help="Definition: directory of the report files.\n"
    "Default: A report directory will be created under current directory",
)
@click.option(
    "--db-dir",
    "-db",
    default=Path.cwd(),
    type=click.Path(),
    help="Definition: directory of the report files.\n"
    "Default: A report directory will be created under current directory",
)
@click.option(
    "--report-format",
    "-f",
    default="csv",
    type=click.Choice(["json", "csv"]),
    help="Definition: output format for your report.\n" "Options: json, csv",
)
@click.option(
    "--error-analysis",
    "-ea",
    is_flag=True,
    default=False,
    help="Whether to create the error analysis report PDF.",
    callback=error_analysis_args
)
@click.option(
    "--doc_dir",
    "-docs",
    required=False,
    type=click.Path(),
    help="Definition: Directory of original pdf or image of the invoices.\n",
)
@click.option(
    "--num_docs",
    "-n_docs",
    default=20,
    help="Definition: The number of invoices contained in the error analysis report.\n"
    "Default: 20",
)
@click.option(
    "--num_vendors",
    "-n_vendors",
    default=10,
    help="Definition: The number of vendors contained in the error analysis report.\n"
    "Default: 10",
)
@click.pass_context
def evaluate(
    ctx,
    job_id,
    ground_truth_file,
    model_1_file,
    model_2_file,
    entities,
    vendor_field,
    report_dir,
    db_dir,
    report_format,
    error_analysis,
    doc_dir,
    num_docs,
    num_vendors
):
    """Evaluate two models' performance against ground truth. """
    ctx.ensure_object(dict)

    ctx.obj["job_id"] = job_id
    ctx.obj["ground_truth_file"] = ground_truth_file
    ctx.obj["model_1_file"] = model_1_file
    ctx.obj["model_2_file"] = model_2_file
    ctx.obj["entities"] = set(entities) or None
    ctx.obj["vendor_field"] = vendor_field
    ctx.obj["report_dir"] = report_dir
    ctx.obj["db_dir"] = db_dir
    ctx.obj["report_format"] = report_format
    ctx.obj["error_analysis"] = error_analysis
    ctx.obj["doc_dir"] = doc_dir
    ctx.obj["num_docs"] = num_docs
    ctx.obj["num_vendors"] = num_vendors

    sns.set_theme(style="whitegrid")

    evaluation = Evaluation(
        job_id=ctx.obj["job_id"],
        ground_truth_file=ctx.obj["ground_truth_file"],
        model_1_file=ctx.obj["model_1_file"],
        model_2_file=ctx.obj["model_2_file"],
        entities=ctx.obj["entities"],
        vendor_field=ctx.obj["vendor_field"],
        db_dir=Path(ctx.obj["db_dir"]),
    )
    output_dir = Path(ctx.obj["report_dir"]) / evaluation.job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    all_reports = {}

    # Model level evaluation report
    print("Creating the model evaluation report.")
    model_report = evaluation.create_report(granularity=Granularity.MODEL)
    all_reports["model"] = model_report
    model_df = pd.DataFrame(data=model_report)
    sns.barplot(x="model_id", y="no_touch_rate", data=model_df)
    plt.xticks(fontsize="x-small")
    plt.savefig(output_dir / "model", bbox_inches="tight")
    plt.clf()

    # Entity level report
    print("Creating the entity evaluation report.")
    entity_report = evaluation.create_report(granularity=Granularity.ENTITY)
    all_reports["entity"] = entity_report
    entity_df = pd.DataFrame(data=entity_report)[:20]
    sns.barplot(y="entity", x="accuracy", hue="model_id", data=entity_df, orient="h")
    plt.yticks(fontsize="x-small")
    plt.legend(bbox_to_anchor=(0, 1.1), loc="upper left", fontsize="x-small")
    plt.savefig(output_dir / "entity", bbox_inches="tight")
    plt.clf()

    if ctx.obj["vendor_field"]:
        print("Creating the vendor evaluation report.")
        vendor_report = evaluation.create_report(granularity=Granularity.VENDOR)
        all_reports["vendor"] = vendor_report

    for report_name, data in all_reports.items():
        if ctx.obj["report_format"] == "json":
            with open(output_dir / f"{report_name}.json", "w") as fp:
                json.dump(data, fp)
        elif ctx.obj["report_format"] == "csv":
            _dict_to_csv(data, output_dir / f"{report_name}.csv")

    print(f"Evaluation reports created: {output_dir.absolute()}")

    if ctx.obj["error_analysis"]:
        print("Creating the error analysis report.")
        entities, query_results = analysis(
            job_id=evaluation.job_id,
            num_vendors=ctx.obj["num_vendors"],
            num_docs=ctx.obj["num_docs"],
            db_dir=Path(ctx.obj["db_dir"])
        )

        pdf = create_error_analysis_report(entities, query_results, Path(ctx.obj["doc_dir"]))
        output_path = output_dir / "error_analysis.pdf"
        pdf.output(output_path, "F")
        print(f"Error analysis created: {output_path.absolute()}")


def _dict_to_csv(data, report_path):
    with open(report_path, "w") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    evaluate(obj={})
