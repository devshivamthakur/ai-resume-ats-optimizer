from jinja2 import Environment, FileSystemLoader
import os

def render_latex(data: dict, output_path: str):
    env = Environment(
        loader=FileSystemLoader("latex"),
        autoescape=False,   # REQUIRED for LaTeX
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="{{",
        variable_end_string="}}",
        comment_start_string="{#",
        comment_end_string="#}",
    )

    template = env.get_template("resume_template.tex")
    rendered_tex = template.render(**data)

    with open(output_path, "w") as f:
        f.write(rendered_tex)
