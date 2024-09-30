import os

class HTMLpreproc:
    class PreprocError(Exception):
        ...
    
    def __init__(
            self,
            live_reload: bool = False,
            load_on_start: bool = True,

            preproc_dir: str = "preproc",
            pretty: bool = True,
            prefix: str = "#[",
            suffix: str = "]",
            indent_spaces: int = 4,
            indent_tags: list[str] = ["html", "head", "body", "div", "script", "style", "form", "ul", "li", "a", "header", "main", "nav"],
            max_loops: int = 100,
            var_file_line_sep: str = ";;",

            flask_features: bool = False
            ) -> None:
        
        self.flask_features = flask_features

        if self.flask_features:
            import flask

            self.flask = flask

        self.live_reload = live_reload
        self.load_on_start = False if live_reload else load_on_start
        
        self.preproc_dir = preproc_dir

        self.max_loops = max_loops 
        self.var_file_line_sep = var_file_line_sep

        self.pretty = pretty

        self.indent_spaces = indent_spaces
        self.indent_tags = indent_tags

        self.prefix = prefix
        self.suffix = suffix

        self.templates  : dict[str, str] = {}
        self.components : dict[str, str] = {}
        self.vars       : dict[str, str] = {}

        if self.load_on_start:
            self.load()

    def load(self):
        for filename in os.listdir(f"{self.preproc_dir}/templates"):
            with open(f"{self.preproc_dir}/templates/{filename}", "r", encoding = "utf-8") as f:
                self.templates[filename.rsplit(".", 1)[0]] = f.read()

        for filename in os.listdir(f"{self.preproc_dir}/components"):
            with open(f"{self.preproc_dir}/components/{filename}", "r", encoding = "utf-8") as f:
                self.components[filename.rsplit(".", 1)[0]] = f.read()
        
        with open(f"{self.preproc_dir}/vars.preproc", "r", encoding = "utf-8") as f:
            for line in f.read().split(self.var_file_line_sep):
                if not line or line == "\n":
                    continue

                name, content = ((x := line.split("=", 1))[0].strip()), x[1].strip()

                self.vars["!" + name] = content

                # name, type_, content = (y := ((x := line.split("=", 1))[0].strip()).split(":", 1))[0], y[1], x[1].strip()

                # self.vars["var:" + name] = self._convert_type(content, type_)

    def make_pretty(self, html: str):
        pretty_html = ""
        prev_tag = ""
        indent_counter = 0

        for line in html.split("\n"):
            tag = line.strip().removeprefix("<").removeprefix("<").split(">")[0].split(" ")[0] if line.strip().startswith("<") else ""
            
            if line.count(tag) == 2 and line.count("<") >= 2 and line.count(">") >= 2 and line.count("/") >= 1:
                tag = ""

            if prev_tag in self.indent_tags:
                indent_counter += 1
            
            elif tag in [f"/{tag}" for tag in self.indent_tags]:
                indent_counter -= 1

            pretty_html += (self.indent_spaces * " ") * indent_counter + line.strip() + "\n"
            
            prev_tag = tag

        return pretty_html

    def process(self, template: str, levels: int = -1):
        if self.live_reload:
            self.load()

        html = self.templates[template]

        if levels == -1:
            count = 0

            while self.prefix in html and self.suffix in html:
                if (count % self.max_loops) == (self.max_loops - 1):
                    raise self.PreprocError(f"nonexistent components or variables AND/OR circularly dependant components (max_loops reached: {self.max_loops})")
                
                for k, v in {**dict(self.components.items()), **dict(self.vars.items())}.items():
                    html = html.replace(self.prefix + k + self.suffix, v)

                count += 1

        else:
            for _ in range(levels):
                for k, v in {**dict(self.components.items()), **dict(self.vars.items())}.items():
                    html = html.replace(self.prefix + k + self.suffix, v)


        if self.pretty:
            html = self.make_pretty(html)
            
        return html
    
    def fl_render(self, template: str, **context):
        if not self.flask_features:
            raise self.PreprocError("To use this function please enable `flask_features`!")
        
        return self.flask.render_template_string(self.process(template), **context)