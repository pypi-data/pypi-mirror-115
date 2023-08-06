import json
import logging
import requests


logger = logging.getLogger()


class ExacClient():

	HOST = "http://exac.hms.harvard.edu/rest"
	BATCH_ENDPOINT = "/bulk/variant/variant"
	HEADERS = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US,en;q=0.9,fr;q=0.8,ru;q=0.7"
	}

	def __init__(self):
		"""
		Example request URL:

		http://exac.hms.harvard.edu/rest/variant/variant/14-21853913-T-C
		"""
		pass

	def get_exac_info(self, vcf_records):
		"""
		Given an interable of VCF records, request annotation info from EXAC API

		Returns a dictionary of the original VCF record information, merged with EXAC INFO

		{
			'chr-pos-ref-alt': {
				'vcf_info': <records from VCF>,
				'exac_info': <new annotations from EXAC>
			}
		}
		"""
		sep = '-'
		query = [
			sep.join([
				str(r.CHROM),
				str(r.POS),
				str(r.REF),
				str(r.ALT[0])])
			for r in vcf_records
		]
		logger.debug(query)

		url = self.HOST + self.BATCH_ENDPOINT
		logger.info("Requesting: " + url)
		resp = requests.post(url, data=json.dumps(query), headers=self.HEADERS)
		logger.debug(resp.text)

		def build_key(r):
			key = sep.join([
				str(r.CHROM),
				str(r.POS),
				str(r.REF),
				str(r.ALT[0])
			])
			return key

		# Merge Exac info with original VCF Records
		ret = {
			build_key(r): {
				'vcf_info': r,
				'exac_info': resp.json()[build_key(r)]
			}
			for r in vcf_records
		}
		return ret