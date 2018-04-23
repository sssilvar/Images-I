import vcf
import numpy as np

if __name__ == '__main__':
    vcf_reader = vcf.Reader(open('test.vcf', 'r'))

    record = next(vcf_reader)
    print(record)
    print(record.CHROM)
