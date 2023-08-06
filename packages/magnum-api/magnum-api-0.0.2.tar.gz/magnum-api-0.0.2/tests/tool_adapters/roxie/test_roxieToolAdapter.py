from unittest import TestCase
from unittest.mock import patch

from magnumapi.tool_adapters.roxie.RoxieToolAdapter import RoxieToolAdapter
from tests.resource_files import create_resources_file_path


class TestRoxieToolAdapter(TestCase):
    @patch("magnumapi.tool_adapters.roxie.RoxieToolAdapter.RoxieToolAdapter.plotly_results")
    def test_parse_roxie_xml_11T(self, mock_show=None):
        # arrange
        roxie_data_xml_path = create_resources_file_path('resources/geometry/roxie/11T/reference/roxieData11T.xml')
        strand_data = RoxieToolAdapter.parse_roxie_xml(roxie_data_xml_path)

        # act
        RoxieToolAdapter.plotly_results(strand_data)

        # assert
        if mock_show is not None:
            mock_show.assert_called()

    def test_parse_roxie_xml_16T(self):
        roxie_data_xml_path = create_resources_file_path('resources/geometry/roxie/16T/reference/roxieData16T.xml')

        # assert
        with self.assertRaises(IndexError):
            RoxieToolAdapter.parse_roxie_xml(roxie_data_xml_path)

