#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kopierer alle .pdf filer som matcher følgende mønster:

(FAGKODE)_(2 TALL)_(V eller H)_(1-3 bokstaver)_(.pdf)

Til en egen mappe.



Oppdaterer også /docs index siden.
@author: tommy
"""

import os
import re
import shutil
import zipfile
import more_itertools


if __name__ == '__main__':
    # Path of this script
    path_here, _ = os.path.split(os.path.realpath(__file__))
    
    # One directory up from the location of this script
    path_start, _ = os.path.split(path_here)
    
    # Directory to move to
    PDF_DIR = 'alle_pdf_filer'
    FAGKODER = {'1P', '2P', '1T', 'S1', 'S2', 'R1', 'R2', '2T'}
    
    shutil.rmtree(os.path.join(path_start, PDF_DIR))
    os.makedirs(os.path.join(path_start, PDF_DIR), exist_ok=True)
    
    # Regex pattern
    fagkoder_joined = '|'.join((f for f in FAGKODER))
    pattern_str = r'(' + fagkoder_joined + r')\_\d{2}(H|V).{0,3}\.pdf'
    pattern = re.compile(pattern_str)
    
    for dirpath, dirnames, filenames in os.walk(path_start):
        
        # Skip the .git folder
        if ('.git' in dirpath) or (PDF_DIR in dirpath):
            continue
        
        # For every filename
        for filename in filenames:
            
            # If the filename does not match the pattern, skip it
            if not pattern.match(filename):
                continue
            
            # The filename matched the pattern, keep going
            copy_from = os.path.join(dirpath, filename)
            copy_to = os.path.join(path_start, PDF_DIR, filename)
            shutil.copy2(copy_from, copy_to)
            print('Copied to:', copy_to)
            
    # Create a new zip file
    file_name = os.path.join(path_start, PDF_DIR, 'vgs_eksamener.zip')
    file_obj = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    with file_obj as open_zip_file:
        
        # Iterate through every copied file
        for copied_file in os.listdir(os.path.join(path_start, PDF_DIR)):
            if not os.path.isfile(os.path.join(path_start, PDF_DIR, copied_file)):
                continue
            
            _, ext = os.path.splitext(copied_file)
            if not ext == '.pdf':
                continue
            
            # Add the file to the .zip
            file_to_zip = os.path.join(path_start, PDF_DIR, copied_file)
            open_zip_file.write(file_to_zip, 
                                arcname = os.path.basename(file_to_zip))
            print('Wrote to .zip file:', os.path.basename(file_to_zip))
            
            
    # -------------------------------------------------------------------------
    github_repo_url = r'https://github.com/matematikk/vgs_eksamener/blob/master/alle_pdf_filer'
    template_path = os.path.join(path_here, '..', 'docs', 'index_template.html')
    out_path = os.path.join(path_here, '..', 'docs', 'index.html')
    with open(template_path, 'r') as html_template:
        html_file = ''.join(l for l in html_template)
    
        for fagkode in FAGKODER:
            html_code = '<ul>'
            print(fagkode)
            
            relevant_files = os.listdir(os.path.join(path_start, PDF_DIR))
            relevant_files = sorted((f for f in relevant_files if fagkode in f),
                                    reverse=True)
            
            print(relevant_files)
            for lf, problem in more_itertools.chunked(relevant_files, 2):
                link_name, _ = os.path.splitext(problem)
                print(os.path.splitext(lf))
                print(lf, problem)
                html_code += f'<li><a href="{github_repo_url}/{problem}" target="_blank">{link_name}</a>'
                html_code += f' [<a href="{github_repo_url}/{lf}" target="_blank">løsning</a>]</li>\n'
            
            html_file = html_file.replace(f'CONTENT_{fagkode}', html_code + '</ul>')
            
            #print(html_file)
        with open(out_path, 'w') as out_file:
            out_file.write(html_file)
        
                
                #<a href="https://github.com/tommyod/matte_eksamener_VGS/blob/master/alle_pdf_filer/S2_15H_lf.pdf" target="_blank">S2_15H_lf.pdf</a>
            #for file in relevant_files:
            #    print(' ', file)
    #print(html_code)
            
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
    