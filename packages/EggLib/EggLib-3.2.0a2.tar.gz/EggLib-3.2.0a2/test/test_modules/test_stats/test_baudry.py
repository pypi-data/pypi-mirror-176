import os, egglib, sys, unittest
from collections import Iterable
path = os.path.dirname(__file__)
path_T=os.path.join(path, 'correct_files')

class ProbaMisoriented_test(unittest.TestCase):
    def test_ProbaMisoriented_T(self):
        PM=egglib.stats.ProbaMisoriented()
        self.assertEqual(str(type(PM)), "<class 'egglib.stats._baudry.ProbaMisoriented'>")

    def test_reset_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented(aln)
        n_sites_a=PM.S
        PM.reset()
        n_sites_b= PM.S
        self.assertTrue(n_sites_a>n_sites_b)

    def test_load_align_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented()
        PM.load_align(aln, egglib.struct_from_labels(aln))
        self.assertTrue(PM.S>0)	

    def test_load_site_T(self):
        PM=egglib.stats.ProbaMisoriented()
        site_null=[[(4,2),(4,3),(3,1)]]
        frq=egglib.Freq()
        frq.from_list(site_null, outgroup=None)
        n_sites_b=PM.S
        PM.load_site(frq)
        n_sites_a=PM.S
        self.assertTrue(n_sites_a>n_sites_b)

    def test_compute_T(self):
        PM=egglib.stats.ProbaMisoriented()
        site=egglib.Site()
        frq=egglib.Freq()
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM.load_align(aln, egglib.struct_from_labels(aln))
        aln2 = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), alphabet=egglib.alphabets.Alphabet('char', 'ATGC?', '-MRSYW'), labels=True)
        site.from_align(aln2, 0)
        frq.from_site(site)
        PM.load_site(frq)
        titv1= PM.TiTv
        PM.compute()
        titv2= PM.TiTv
        self.assertAlmostEqual(titv1,4.02298850575, 11)
        self.assertAlmostEqual(titv2,3.97727272727, 11)

    def test_S_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented()
        PM.load_align(aln, egglib.struct_from_labels(aln))
        self.assertEqual(PM.S, 241)

    def test_D_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented()
        PM.load_align(aln, egglib.struct_from_labels(aln))
        self.assertEqual(PM.D, 25)

    def test_TiTv_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented()
        PM.load_align(aln, struct=egglib.struct_from_labels(aln))
        self.assertAlmostEqual(PM.TiTv, 4.02298850575, 11)

    def test_pM_T(self):
        aln = egglib.io.from_fasta(os.path.join(path_T, 'dmi3.fas'), labels=True, alphabet=egglib.alphabets.DNA)
        PM=egglib.stats.ProbaMisoriented()
        PM.load_align(aln, egglib.struct_from_labels(aln))
        self.assertAlmostEqual(PM.pM, 0.141393462231, 12)
