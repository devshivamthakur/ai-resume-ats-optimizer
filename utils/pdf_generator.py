import subprocess, os

def generate_pdf(tex_path, workdir):
    subprocess.run(["pdflatex", tex_path], cwd=workdir)
