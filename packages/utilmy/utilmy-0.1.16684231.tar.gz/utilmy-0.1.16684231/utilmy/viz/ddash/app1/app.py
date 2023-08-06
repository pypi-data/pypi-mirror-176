# -*- coding: utf-8 -*-
"""  Launch app
Doc::

    Dependencies
        pip install fire dash dash_bootstrap_components dash_treeview_antd
    
    
    Command to run
        cd utilmy/viz/ddash/app1
        - Launch links viz:       python app.py main --content_layout assets/links_layout.json
        - Launch html viz:        python app.py main --content_layout assets/html_layout.json --homepage main.html
        - Launch dash pages viz:  python app.py main --content_layout assets/dash_layout.json --homepage main_page.py  
    
    
    2. Data
        copy .html files to assets/html/
        copy pages.py files to pages/ folder      - For Dash Pages:

    
    3. Layout Json, Example,     Save layout .json to *assets* folder    
        {
            "main_content" : {   #### CSS Style in JSON Format, Applied to main content. ex :   
                "marginLeft": "20%",
                "height":     "100vh"
            },


            ####  key with this 3 types of target-render will automatically loaded in main content
            "sidebar_content":{
                "version": 1,   ### Number. The latest Update only support for version 1.
                "data": { "title": "Home", 
                          "key":"https://gallery.plotly.host/bball-shot-explorer",
                                "children": [{
                                    "title": "Child",   "key": "01",
                                    "children": [
                                        {"title": "link1", "key": "https://dash.gallery/self-driving/"}
                                    ]   },


                        { "title": "Child2",   
                          "key": "02",
                                "children": [
                                    {"title": "html-1", "key": "page1.html"},
                                    {"title": "html-2", "key": "page2.html"},
                                    {"title": "html-3", "key": "page2_1.html"},

                                    {"title": "dash-1", "key": "page1.py"},
                                    {"title": "dash-2", "key": "page2.py"}
                                ]  }]
                    },

                "style": {  ###  CSS Style in JSON Format
                    "position": "fixed",
                    "top": 0,
                    "left": 0,
                    "bottom": 0,
                    "width": "20%",
                    "padding": "20px 10px",
                    "backgroundColor": "#f8f9fa",
                    "verticalAlign": "middle",
                    "alignItems": "center"
                }
                
            }
        }

        
        - <NUMBER>        : key with Number will flagged as non target-render
    
    
"""
app = None
try :
    import dash_bootstrap_components as dbc
    import os, shutil, importlib, json
    from dash import Dash, html
    from dash.dcc import Store
    from dash.dependencies import ClientsideFunction, Input, Output
    from dash_treeview_antd import TreeView

    app = Dash( __name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True
                )
    app.title = 'Simple render html'

    pages = {}
except : pass



#####################################################################
def test1(homepage="main_page.py"):
    """  python  app.py test1
    Docs::    
    
        homepage (str, optional): _description_. Defaults to "main_page.py".
    """
    import utilmy as uu  
    dir_repo, dir_tmp = uu.dir_testinfo()
    cmd = f"cd {dir_repo}/viz/ddash/app1/  && python app.py main --content_layout assets/dash_layout.json --homepage {homepage} & sleep 10 && curl -Is 127.0.0.1:8050 | head -n 1 && pkill -f 'python app.py' "
    os.system(cmd)


def test2(homepage="main.html"):
    """  python  app.py test2
    Docs::    
    
        python app.py main --content_layout assets/html_layout.json --homepage main.html
        
    """
    import utilmy as uu
    dir_repo, dir_tmp = uu.dir_testinfo()
    cmd = f"cd {dir_repo}/viz/ddash/app1/  && python app.py main --content_layout assets/html_layout.json --homepage {homepage} & sleep 10 && curl -Is 127.0.0.1:8050 | head -n 1 && pkill -f 'python app.py'  "
    os.system(cmd)
    

def test3(homepage="about:blank"):
    """  python  app.py test3
    Docs::    
    
        homepage (str, optional): _description_. Defaults to "about:blank".
    """
    import utilmy as uu
    dir_repo, dir_tmp = uu.dir_testinfo()
    cmd = f"cd {dir_repo}/viz/ddash/app1/  && python app.py main --content_layout assets/links_layout.json --homepage {homepage} & sleep 10 && curl -Is 127.0.0.1:8050 | head -n 1 && pkill -f 'python app.py' "
    os.system(cmd)


def test4(homepage="main_page.py"):
    """  python  app.py test4
    Docs::    
    
        python app.py main --content_layout assets/mixed_layout.json --homepage main_page.py
        
    """
    import utilmy as uu
    dir_repo, dir_tmp = uu.dir_testinfo()
    cmd = f"cd {dir_repo}/viz/ddash/app1/  && python app.py main --content_layout assets/mixed_layout.json --homepage {homepage} & sleep 10 && curl -Is 127.0.0.1:8050 | head -n 1 && pkill -f 'python app.py' "
    os.system(cmd)


###################################################################
def export(name="app1", dirout=""):
    """  python  app.py export
    Docs::    
    
        name (str, optional): _description_. Defaults to "app1".
        dirout (str, optional): _description_. Defaults to Current Working Directory.
    """
    import utilmy
    
    dirout = dirout or os.getcwd()
    dirout = dirout + '/' + name

    dir_repo, dir_tmp = utilmy.dir_testinfo()
    
    os.makedirs(dirout, exist_ok=True)
    shutil.copytree( dir_repo + "/viz/ddash/app1/", dirout, dirs_exist_ok=True )


###################################################################
######  Utils #####################################################
### Main page resource
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='render'
    ),
    Output('target-render', 'data'),
    [Input('input', 'selected'),
    Input('homepage', 'data')]
)


@app.callback(Output('output', 'children'), Input('target-render', 'data'), prevent_initial_call=True)
def html_components(data):
    if data.endswith('.py'):
        page = data.split('/')[-1][:-len('.py')]
        return pages[page].layout
    return html.Iframe(src=data, width='100%', height='100%')
        

###################################################################
def sidebar_v1(sidebar):
    """ Compose Sidebar v1 layout component.
    Docs::

        Args:
            _type_: (dict) Sidebar data and style

        Returns:
            _type_: (dash.html.Div.Div) Sidebar v1 Div Component

        Raises:
            ValueError
                Raised if data or style is not exist in sidebar_content json.
    """
    if 'data' not in sidebar.keys():
        raise ValueError('data key not found in json file')
    
    if 'style' not in sidebar.keys():
        raise ValueError('style key not found in json file')

    sidebar_content = html.Div( 
                        TreeView(
                            id='input',
                            multiple=False,
                            checkable=False,
                            checked=False,
                            selected=[],
                            expanded=[],
                            data=sidebar['data']
                        ), style=sidebar['style']
                    )
    return sidebar_content


def render_page(content_layout, homepage):
    """Main Render Page
    Docs::

        Raises:
            ValueError
                - Raised if sidebar_content is not found in layout json.
                - Raised if version is not found in sidebar_content section.
    
    """
    SIDEBAR_VER = {1: sidebar_v1} # Scalable sidebar

    if 'sidebar_content' not in content_layout.keys():
        raise ValueError('sidebar_content key not found in layout json')
    
    if 'version' not in content_layout['sidebar_content'].keys():
        raise ValueError('version key not found in sidebar_content section')
        
    version = content_layout['sidebar_content']['version'] 

    sidebar_content = SIDEBAR_VER[version](content_layout['sidebar_content'])
    main_content = html.Div(id="output", style=content_layout['main_content'])

    app.layout = html.Div([
                            sidebar_content, 
                            main_content,
                            Store(id='homepage', storage_type='session', data=homepage),
                            Store(id='target-render'), 
                            ])


def main(content_layout="assets/html_layout.json", homepage="", debug=True, dir_log=""):
    """ Run main app
    Docs::

        Args:
            content_layout (dict, optional):
                The content layout in JSON format. Default to 'assets/html_layout.json'.
            homepage (str, optional): 
                Set Homepage Location. Defaults to "None".
            debug (boolean, optional):
                Set dash debug options. Default to 'True'
    
        Raises:
            ValueError
                Raised if content_type is not 'links', 'html', or 'dash'.
    """
    global pages

    try:
        for page in [f for f in os.listdir('pages') if f.endswith('.py')]:
            page = page[:-3]
            pages[page] = importlib.import_module('pages.' + page)
    except Exception as e:
        print(f'Error importing dash page module. {e}')
    
    with open(fr"{content_layout}", "rb") as f:
        content_layout = json.loads(f.read())

    homepage = homepage or content_layout['sidebar_content']['data']['key']
   
    render_page(content_layout, homepage)

    app.run_server(debug=debug)


if __name__ == '__main__':
     import fire
     fire.Fire()

