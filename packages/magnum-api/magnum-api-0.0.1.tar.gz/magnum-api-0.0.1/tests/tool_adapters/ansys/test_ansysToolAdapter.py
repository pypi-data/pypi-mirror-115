import unittest
from unittest.mock import patch

import numpy as np

from magnumapi.geometry.CosThetaGeometry import HomogenizedCosThetaGeometry
from magnumapi.geometry.GeometryFactory import GeometryFactory
from magnumapi.geometry.roxie.CableDatabase import CableDatabase
from magnumapi.tool_adapters.ansys.AnsysToolAdapter import AnsysToolAdapter
from magnumapi.tool_adapters.roxie.RoxieToolAdapter import RoxieToolAdapter
from tests.resource_files import create_resources_file_path


class TestAnsysToolAdapter(unittest.TestCase):
    @patch("matplotlib.pyplot.show")
    def test_input_file_generation(self, mock_show=None):

        json_path = create_resources_file_path('resources/geometry/roxie/16T/16T_rel.json')
        cadata_path = create_resources_file_path('resources/geometry/roxie/16T/roxieold_2.cadata')
        cadata = CableDatabase.read_cadata(cadata_path)

        geometry = GeometryFactory.init_with_json(json_path, cadata)
        geometry.build_blocks()
        geometry.plot_blocks()

        homo_geometry = HomogenizedCosThetaGeometry.with_cos_theta_geometry(geometry)

        # Find number of layers
        n_layers = homo_geometry.get_number_of_layers()

        self.assertEqual(4, n_layers)
        # For each layer
        # # Number of blocks per layer
        blocks_per_layer = homo_geometry.get_number_of_blocks_per_layer()
        self.assertListEqual([4, 3, 3, 2], blocks_per_layer)

        # # write inner radius - taken as the minimum radius out of all all radii of a layer
        inner_radii = HomogenizedCosThetaGeometry.get_inner_radii(geometry)

        inner_radii_ref = [25.000000000000004, 39.0, 53.0, 67.45000006216533]
        np.testing.assert_allclose(inner_radii_ref, inner_radii)

        # # write inner radius - taken as the minimum radius out of all radii of a layer
        outer_radii = HomogenizedCosThetaGeometry.get_outer_radii(geometry)

        outer_radii_ref = [38.514032903286974, 52.513971821900164, 66.87212964199654, 81.3221676585706]
        np.testing.assert_allclose(outer_radii_ref, outer_radii)

        output_text = AnsysToolAdapter.prepare_ansys_model_input(homo_geometry)
        output_text_ref_path = create_resources_file_path('resources/tool_adapters/ansys/Model.inp')
        with open(output_text_ref_path, 'r') as file:
            output_text_ref = file.readlines()

        self.assertListEqual(output_text_ref, output_text)

        if mock_show is not None:
            mock_show.assert_called()

    def test_roxie_force_to_ansys(self):
        # arrange
        roxie_force_input_path = create_resources_file_path('resources/tool_adapters/ansys/roxie.force2d')
        roxie_force_output_path = create_resources_file_path('resources/tool_adapters/ansys/roxie_edit.force2d')
        ansys_force_output_path = create_resources_file_path('resources/tool_adapters/ansys/forces_edit.vallone')
        field = 15
        target_field = 16

        # act
        # # update ROXIE force file
        RoxieToolAdapter.update_force2d_with_field_scaling(roxie_force_input_path,
                                                           roxie_force_output_path,
                                                           field,
                                                           target_field)

        # # prepare ANSYS force file
        AnsysToolAdapter.prepare_force_file(roxie_force_output_path, ansys_force_output_path)

        # assert
        with open(ansys_force_output_path, 'r') as file:
            ansys_force = file.readlines()

        output_text_ref_path = create_resources_file_path('resources/tool_adapters/ansys/forces_edit_ref.vallone')

        with open(output_text_ref_path, 'r') as file:
            ansys_force_ref = file.readlines()

        for ansys_force_ref_el, ansys_force_el in zip(ansys_force_ref, ansys_force):
            self.assertEqual(ansys_force_ref_el, ansys_force_el)


if __name__ == '__main__':
    unittest.main()
