import os
from subprocess import Popen, PIPE

import pandas as pd

from magnumapi.geometry.CosThetaGeometry import HomogenizedCosThetaGeometry
from magnumapi.tool_adapters.ToolAdapter import ToolAdapter

print('Loaded Tool Adapter version 0.0.1 for ANSYS2020R2')


class AnsysToolAdapter(ToolAdapter):

    def __init__(self,
                 ansys_path: str,
                 rel_dir: str,
                 inp_path: str,
                 out_path: str,
                 output_file: str
                 ) -> None:
        self.ansys_path = ansys_path
        self.rel_dir = rel_dir
        self.inp_path = inp_path
        self.out_path = out_path
        self.output_file = output_file
        self.output_lines = []

    def run(self) -> None:
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)
        else:  ## Show an error ##
            print("Warning: %s file not found" % self.output_file)

        p = Popen([self.ansys_path, '-b', '-p', '-aa_r', '-smp', '-np', '2', '-lch', '-dir', self.rel_dir, '-i',
                   self.inp_path, '-o', self.out_path],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        byte_output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode

        byte_output_decode = byte_output.decode()
        self.output_lines = byte_output_decode.split('\n')

    def read_figures_of_merit_table(self) -> pd.DataFrame:
        with open(self.output_file, 'r') as output:
            output_file_content = output.read().split('\n')

        keys = output_file_content[0].split(' ')
        keys = [key for key in keys if key != '']

        values = output_file_content[1].split(' ')
        values = [float(value) for value in values if value != '']

        key_value = {key: value for key, value in zip(keys, values)}
        return pd.DataFrame(key_value, index=[0])

    @staticmethod
    def convert_figures_of_merit_to_dict(fom_df: pd.DataFrame) -> dict:
        return fom_df.to_dict('records')[0]

    @classmethod
    def write_ansys_input_text(cls, file_path: str, geometry: HomogenizedCosThetaGeometry) -> None:
        n_layers = geometry.get_number_of_layers()
        blocks_per_layer = geometry.get_number_of_blocks_per_layer()
        output_text = cls.generate_ansys_input_text(geometry, n_layers, blocks_per_layer)

        with open(file_path, 'w') as file:
            for output_text_el in output_text:
                file.write(output_text_el)

    @staticmethod
    def generate_ansys_input_text(geometry: HomogenizedCosThetaGeometry, n_layers, blocks_per_layer):
        output_text = []
        output_text.append('! Example Input File\n')
        output_text.append('! -------------------\n')
        output_text.append('! - Standard\n')
        output_text.append('/UNITS,SI\n')
        output_text.append('pi = acos(-1)\n')
        output_text.append('*afun,deg		 ! Specifies the units for angular functions in parameter expressions\n')
        output_text.append('tref,293\n')
        output_text.append('! -------------------\n')
        output_text.append('! Set-up arrays\n')
        output_text.append('! *dim,V_Field,array,1,1\n')
        output_text.append('! *dim,V_Nlay,array,1,1\n')
        output_text.append('! *dim,V_blocks,array,1,1\n')
        output_text.append('! *dim,V_current,array,1,1\n')
        output_text.append('! *dim,V_rad,array,1,2\n')
        output_text.append('! *dim,V_turns,array,1,1\n')
        output_text.append('! *dim,V_corners,array,2,4\n')
        output_text.append('\n')
        output_text.append('! General\n')

        output_text.append('Nlay = %d\n' % n_layers)
        output_text.append('\n')

        radius_inner_prev = None
        index_layer = -1
        index_block = 0
        for block in geometry.blocks:
            if radius_inner_prev != block.homo_block_def.radius_inner:
                index_block = 0
                index_layer += 1
                output_text.append('! Layer\n')
                output_text.append('Nb%d = %d\n' % (index_layer + 1, blocks_per_layer[index_layer]))
                output_text.append('current%d = %f\n' % (index_layer + 1, block.homo_block_def.current))
                output_text.append('r%d1 = %fe-3\n' % (index_layer + 1, block.homo_block_def.radius_inner))
                output_text.append('r%d2 = %fe-3\n' % (index_layer + 1, block.homo_block_def.radius_outer))

            output_text.append('! Block\n')
            output_text.append('Nc%d%d = %d\n' % (index_layer + 1, index_block + 1, block.homo_block_def.nco))
            output_text.append('\n')
            output_text.append('! Save angles\n')
            output_text.append('t%d%d_1 = %.4f\n' % (index_layer + 1, index_block + 1, block.homo_block_def.phi_0))
            output_text.append('t%d%d_2 = %.4f\n' % (index_layer + 1, index_block + 1, block.homo_block_def.phi_1))
            output_text.append('t%d%d_3 = %.4f\n' % (index_layer + 1, index_block + 1, block.homo_block_def.phi_2))
            output_text.append('t%d%d_4 = %.4f\n' % (index_layer + 1, index_block + 1, block.homo_block_def.phi_3))

            if index_block + 1 == blocks_per_layer[index_layer]:
                # Fixes the first 2 angles of the 1st block to be 0 / assumes mid-plane shim thickness = 0
                output_text.append('\n')
                output_text.append('t%d1_1 = 0\n' % (index_layer + 1))
                output_text.append('t%d1_2 = 0\n' % (index_layer + 1))
                output_text.append('\n')

            index_block += 1
            radius_inner_prev = block.homo_block_def.radius_inner

        output_text.append('! Names\n')
        output_text.append('r1 = r11\n')
        output_text.append('r%d = r%d2\n' % (n_layers + 1, n_layers))
        output_text.append('rout = r%d\n' % (n_layers + 1))
        output_text.append('Nlayers = Nlay\n')

        output_text.append('\n')
        output_text.append('! -------------------------------------\n')
        output_text.append('! - Geometry parameters\n')
        output_text.append('! ---- Filler\n')
        output_text.append('*set, fillerth, 5e-3\n')

        output_text.append('\n')
        output_text.append('! ---- Yoke\n')
        output_text.append('*set,yoketh,260e-3\n')

        output_text.append('\n')
        output_text.append('! Update geometry\n')
        output_text.append('*set, rin_yoke, rout + fillerth\n')
        output_text.append('*set, rout_yoke, rin_yoke + yoketh\n')

        output_text.append('\n')
        output_text.append('! -------------------------------------\n')
        output_text.append('! Interlay Contact - Filler is Nlayers+1\n')
        output_text.append('! Glue = 5 , Sliding = 0\n')
        output_text.append('ilay_12 = 5\n')
        output_text.append('ilay_23 = 0\n')
        output_text.append('ilay_34 = 5\n')
        output_text.append('ilay_45 = 0\n')
        output_text.append('! -------------------------------------\n')
        output_text.append('! Mesh Parameters\n')
        output_text.append('mpar = 1\n')
        output_text.append('\n')
        output_text.append('mesh_azim_size = mpar*2e-3    ! Coil Azimuthal\n')
        output_text.append('mesh_radial_size = mpar*2e-3    ! Coil Radial\n')
        output_text.append('\n')
        output_text.append('msize_aperture = mpar*1e-3\n')
        output_text.append('msize_filler = mpar*3e-3\n')
        output_text.append('msize_yoke = mpar*10e-3\n')
        output_text.append('\n')
        output_text.append('!!!!!!!!!!!!!!!!!!!!!!!\n')
        output_text.append('! Friction Parameters !\n')
        output_text.append('!!!!!!!!!!!!!!!!!!!!!!!\n')
        output_text.append('mu_single = 0.0\n')
        output_text.append('mu_g10_coil = mu_single\n')
        output_text.append('mu_ti_coil = mu_single\n')
        output_text.append('mu_ti_g10 = mu_single\n')
        output_text.append('mu_g10_ss = mu_single\n')
        output_text.append('mu_alu_iron = mu_single\n')
        output_text.append('mu_ss_ss = mu_single\n')
        output_text.append('mu_ss_ti = mu_single\n')
        output_text.append('mu_ss_iron = mu_single\n')

        return output_text

    @staticmethod
    def prepare_force_file(force_input_path, force_output_path):
        with open(force_input_path, 'r') as file_read:
            force_txt = file_read.readlines()

        ansys_force = []
        for force_txt_el in force_txt:
            row_float = [float(el) for el in force_txt_el.replace('\n', '').split(' ') if el != '']
            ansys_force.append('nodeNum = NODE(%f, %f, 0.0)' % tuple(row_float[:2]))
            ansys_force.append('F,nodeNum,FX, %f' % row_float[2])
            ansys_force.append('F,nodeNum,FY, %f' % row_float[3])

        with open(force_output_path, 'w') as file_write:
            for ansys_force_el in ansys_force:
                file_write.write(ansys_force_el + '\n')

    @staticmethod
    def write_geometry_input_file(homo_geometry, model_path):
        output_text = AnsysToolAdapter.prepare_ansys_model_input(homo_geometry)

        with open(model_path, 'w') as file_write:
            for output_text_el in output_text:
                file_write.write(output_text_el + '\n')

    @staticmethod
    def prepare_ansys_model_input(homo_geometry):
        n_layers = homo_geometry.get_number_of_layers()
        blocks_per_layer = homo_geometry.get_number_of_blocks_per_layer()
        output_text = AnsysToolAdapter.generate_ansys_input_text(homo_geometry, n_layers, blocks_per_layer)
        return output_text
