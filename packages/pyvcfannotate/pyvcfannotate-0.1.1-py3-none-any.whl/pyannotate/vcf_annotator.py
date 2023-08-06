# Todo:
# What is the difference b/w AC and AO?
# Option to write to either VCF or MAF
# Allow choosing from multiple available ALTs
# Explore output using vcfwriter class
# Handle multiple transcripts

import csv
import vcf
import json
import logging
import requests
import itertools

from pyannotate.exac_client import ExacClient


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

class VCFAnnotator():

	# Variants per request
	BATCH_REQUEST_SIZE = 1000
	OUT_HEADER = [
		'CHROM',
		'POS',
		'REF',
		'ALT',
		'DP',
		'AC',
		'AF',
		'TYPE',
		'EXAC_AF',
		'VEP_EFFECT'
	]
	RANKED_CONSEQUENCES = {
		'transcript_ablation': 1,
		'splice_acceptor_variant': 2,
		'splice_donor_variant': 3,
		'stop_gained': 4,
		'frameshift_variant': 5,
		'stop_lost': 6,
		'start_lost': 7,
		'transcript_amplification': 8,
		'inframe_insertion': 9,
		'inframe_deletion': 10,
		'missense_variant': 11,
		'protein_altering_variant': 12,
		'splice_region_variant': 13,
		'incomplete_terminal_codon_variant': 14,
		'start_retained_variant': 15,
		'stop_retained_variant': 16,
		'synonymous_variant': 17,
		'coding_sequence_variant': 18,
		'mature_miRNA_variant': 19,
		'5_prime_UTR_variant': 20,
		'3_prime_UTR_variant': 21,
		'non_coding_transcript_exon_variant': 22,
		'intron_variant': 23,
		'NMD_transcript_variant': 24,
		'non_coding_transcript_variant': 25,
		'upstream_gene_variant': 26,
		'downstream_gene_variant': 27,
		'TFBS_ablation': 28,
		'TFBS_amplification': 29,
		'TF_binding_site_variant': 30,
		'regulatory_region_ablation': 31,
		'regulatory_region_amplification': 32,
		'feature_elongation': 33,
		'regulatory_region_variant': 34,
		'feature_truncation': 35,
		'intergenic_variant': 36
	}


	def __init__(self, batch_request_size=1000):
		"""Create new VCFAnnotator instance"""
		self.BATCH_REQUEST_SIZE = batch_request_size


	def annotate_vcf(self, vcf_path, output_vcf_path=None):
		"""
		Read and parse records from vcf_path

		Write output records to output_vcf_path, with Exac Annotation information
		"""
		exac_cli = ExacClient()

		if not output_vcf_path:
			output_vcf_path = vcf_path.replace('.vcf', '_annotated.maf')
		vcf_reader = vcf.Reader(open(vcf_path, 'r'))

		with open(output_vcf_path, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter='\t')
			writer.writerow(self.OUT_HEADER)

			for records in self.grouper(self.BATCH_REQUEST_SIZE, vcf_reader):
				logger.debug(records)
				records_with_exac = exac_cli.get_exac_info(records)
				exac_af = '-'

				for k, v in records_with_exac.items():
					# Extract EXAC allele frequency
					exac_af = '-'
					if 'allele_freq' in v['exac_info']:
						exac_af = v['exac_info']['allele_freq']

					# Find most deleterious effect
					major_effect = '-'
					if 'vep_annotations' in v['exac_info']:
						vep_annotations = v['exac_info']['vep_annotations']
						vep_effects = [e['major_consequence'] for e in vep_annotations]
						if len(vep_effects):
							major_effect = vep_effects[0]
							for e in vep_effects:
								if self.RANKED_CONSEQUENCES[e] < self.RANKED_CONSEQUENCES[major_effect]:
									major_effect = e

					inf = v['vcf_info']
					inf_info = inf.INFO
					out = [
						inf.CHROM,
						inf.POS,
						inf.REF,
						inf.ALT[0],
						inf_info['DP'],
						inf_info['AC'][0],
						inf_info['AF'][0],
						inf_info['TYPE'][0],
						exac_af,
						major_effect
					]
					writer.writerow(out)


	def grouper(self, n, iterable):
	    it = iter(iterable)
	    while True:
	        chunk = tuple(itertools.islice(it, n))
	        if not chunk:
	            return
	        yield chunk