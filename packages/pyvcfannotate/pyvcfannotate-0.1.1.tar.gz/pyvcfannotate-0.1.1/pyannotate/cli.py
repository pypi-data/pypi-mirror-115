import os
import click

from pyannotate.vcf_annotator import VCFAnnotator


@click.command()
@click.option("--vcf_path", required=True, help="Path to input VCF")
@click.option("--output_vcf_path", required=False, help="Path to output VCF")
def annotate(vcf_path, output_vcf_path):
	"""
	"""
	# Use absolute paths
	vcf_path = os.path.abspath(vcf_path)
	if output_vcf_path:
		output_vcf_path = os.path.abspath(output_vcf_path)

	annotator = VCFAnnotator()
	annotator.annotate_vcf(vcf_path, output_vcf_path)
