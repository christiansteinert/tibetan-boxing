import os
import sys
import subprocess
import re
import json
import tempfile

import io


# 3rd party dependencies:
from flask import Flask, request, Response

app = Flask(__name__)
config = {}

def init():
    global config
    return

def get_own_path():
    return os.path.dirname(__file__)

def load_config():
    try:
        with open(f'{get_own_path()}/data/config.json', encoding="utf-8") as config_file:
            config = json.load(config_file)            
        return config
    except Exception as e:
        print(e)

def sanitize_input(text:str):
    # remove special chars that are relevant for LaTex parsing
    text = text.replace('$','')
    text = text.replace('\\','')
    return text

def get_template_path():
    return get_own_path() + '/template.tex'

def exec(cmd):
    print(' '.join(cmd))
    subprocess.run(cmd, shell=False, check=True)

def escape_tex(tex_code):
    return re.sub(r'([_{}\\])', r'\\\1', tex_code)
    

def generate_box(tibetan:str, above:str, below:str, has_border:bool):
    # recursive processing to  allow for nested boxes
    tibetan = generate_boxes_for_chunk(tibetan)
    above = generate_boxes_for_chunk(above)
    below = generate_boxes_for_chunk(below)

    # generate boxes for the current chunk
    if has_border:
        if not above and not below:
            return f'\\boxOnly{{{tibetan}}}'
        else:
            return f'\\tibAboveBelow{{{tibetan}}}{{{above}}}{{{below}}}'
    else:
        if not above and not below:
            return tibetan 
        else:
            return f'\\tibAboveBelowNoBorder{{{tibetan}}}{{{above}}}{{{below}}}'

def generate_boxes_for_chunk(text:str):
    if not text:
        return ''

    result = ''
    start_pos, end_pos, nesting, pos = 0, 0, 0, 0
    colons = []

    for idx, char in enumerate(text):
        if char == '(' or char == '[':
            nesting += 1 
            if nesting == 1:
                start_pos = idx
                colons = []

        elif char == ')' or char == ']':
            if nesting == 1:
                end_pos = idx
                result += text[pos:start_pos].strip()

                if len(colons) == 0:
                    colons.insert(0,start_pos)
                    colons.insert(0,start_pos)
                elif len(colons) == 1:
                    colons.insert(1,colons[0])

                below = text[start_pos + 1:colons[0]].strip()
                above = text[colons[0]+1:colons[1]].strip()
                tibetan = text[colons[1]+1:end_pos].strip()

                result += generate_box(tibetan, above, below, char == ']')

                pos = idx + 1

            if nesting > 0:
                nesting -= 1 
        
        elif char == ':' and nesting == 1:
            colons.append(idx)

    result += escape_tex(text[pos:].strip())
    return result

def merge_multiline_tibetan(markdown_text:str):
    """
    If a block of Tibetan spans multiple lines, we merge them into a single one.
    This allows to add line breaks in the code more easily so that the lines in the source 
    text do not become too long
    """
    result = ''
    inside_tib_block = False
    
    for line in markdown_text.split('\n'):
        if line.startswith('> ') or line.startswith('>> '):
            if inside_tib_block:
                # we are continuing within a Tibetan block -> merge with the previous line
                result += ' ' + line[2:].strip()
            else:
                result += '\n' + line

            inside_tib_block = True
        else:
            inside_tib_block = False
            result += '\n' + line
    return result
        
def generate_boxes(markdown_text:str):
    lines = []

    markdown_text = merge_multiline_tibetan(markdown_text)
    for line in markdown_text.split('\n'):
        if line.startswith('> ') or line.startswith('>> '):
            # blockquote line -> do boxing
            prefix = '> ' if line.startswith('>> ') else ''
            line_content = generate_boxes_for_chunk(line[2:].strip())
            lines.append( f'{prefix}\\tibetanfont{{{line_content}}}\\englishfont' )
        else:
            # normal line -> no boxing
            lines.append( line )
        
    return '\n'.join(lines)


def convert_markdown(markdown_text:str, format:str='latex'):
    """
    Converts markdown to text

    Parameters:
    - markdown_text: The markdown code to be converted 
    - format: target format - 'latex' or 'pdf'
    """
    os.chdir('/tmp')

    markdown_text = generate_boxes(markdown_text)

    md_file = tempfile.NamedTemporaryFile(prefix='boxing_', suffix='.md', delete=False) 
    base_name = md_file.name.replace('.md','')
    tex_file_name = base_name + '.tex'

    with md_file:
        md_file.write(markdown_text.encode('utf-8'))

    exec([
        '/usr/bin/pandoc',
        md_file.name, 
        f'--template={get_template_path()}',
        '-t', 'latex',
        '-s',
        '-o', tex_file_name,
    ])

    os.remove(md_file.name)

    if format == 'latex':
        with open(tex_file_name,'r') as tex_file:
            tex = tex_file.read()    
        os.remove(tex_file_name)    
        return tex
    elif format == 'pdf':
        exec([
            '/usr/bin/xelatex',
            '-synctex=1',
            '-no-shell-escape'
            '-output-directory=/tmp'
            '-interaction=nonstopmode',
            tex_file_name,
        ])

        pdf_file_name = base_name + '.pdf'
        print(pdf_file_name)
        with open(pdf_file_name, 'rb') as pdf_file:
            pdf = pdf_file.read()

        os.remove(tex_file_name)    
        os.remove(pdf_file_name)
        os.remove(base_name + '.aux')
        os.remove(base_name + '.log')
        os.remove(base_name + '.synctex.gz')
        
        return pdf


@app.route('/latex', methods=['POST'])
def generate_latex():
    markdown = request.form["textInput"] 
    markdown = sanitize_input(markdown)
    
    latex = convert_markdown(markdown, format='latex')

    return Response(latex, mimetype='text/plain', headers={'Content-Disposition': 'inline; filename="BoxedTibetan.tex'})


@app.route('/pdf', methods=['POST'])
def generate_pdf():
    markdown = request.form["textInput"] 
    markdown = sanitize_input(markdown)
    
    pdf = convert_markdown(markdown, format='pdf')

    return Response(pdf, mimetype='application/pdf', headers={'X-XContent-Disposition': 'inline; filename="BoxedTibetan.pdf'})

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # test mode: run directly via command line if the file name of a markdown file is passed
        with open(sys.argv[1],'r') as md_file:
            markdown = md_file.read()    
            print(convert_markdown(markdown, 'pdf'))
    else:
        # regular mode: run as flask web application
        app.run()
    
application = app
