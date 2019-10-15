import unittest
import cell_line_pax


class TestCellLinePax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.src = cell_line_pax
    
    def test_organize_observation(self):
        input_0 = [{'protein_id':{'uniprot_id': 'id_0'}, 'abundance': '0.0'},
                   {'protein_id':{'uniprot_id': 'id_1'}, 'abundance': '1.0'},
                   {'protein_id':{'uniprot_id': 'id_2'}, 'abundance': '2.0'}]
        exp_0 = {'id_0': [0.0], 'id_1': [1.0], 'id_2': [2.0]}
        result_0 = self.src.organize_observation(input_0, {})
        self.assertEqual(exp_0, result_0)
        input_1 = [{'protein_id':{'uniprot_id': 'id_0'}, 'abundance': '1.0'},
                   {'protein_id':{'uniprot_id': 'id_1'}, 'abundance': '2.0'},
                   {'protein_id':{'uniprot_id': 'id_3'}, 'abundance': '2.0'}]
        exp_1 = {'id_0': [0.0, 1.0], 'id_1': [1.0, 2.0], 'id_2': [2.0, None], 'id_3': [None, 2.0]}
        result_1 = self.src.organize_observation(input_1, exp_0)
        self.assertEqual(exp_1, result_1)
        input_2 = [{'protein_id':{'uniprot_id': 'id_4'}, 'abundance': '1.0'},
                   {'protein_id':{'uniprot_id': 'id_5'}, 'abundance': '2.0'},
                   {'protein_id':{'uniprot_id': 'id_6'}, 'abundance': '2.0'}]
        exp_2 = {'id_0': [0.0, 1.0, None], 'id_1': [1.0, 2.0, None], 
                'id_2': [2.0, None, None], 'id_3': [None, 2.0, None],
                'id_4': [None, None, 1.0], 'id_5': [None, None, 2.0], 'id_6': [None, None, 2.0]}
        result_2 = self.src.organize_observation(input_2, exp_1)
        self.assertEqual(exp_2, result_2)

    def test_get_distinct_publications(self):
        result = self.src.get_distinct_publications()
        self.assertTrue('http://www.mcponline.org/cgi/doi/10.1074/mcp.M111.014050' in result)