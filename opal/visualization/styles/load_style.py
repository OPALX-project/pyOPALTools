def load_style(use='default'):
    from opal.visualization.styles.default import default
    from opal.visualization.styles.jupyter import jupyter
    from opal.visualization.styles.poster import poster
    
    styles = [
        'default',
        'jupyter',
        'poster'
    ]
    
    if use in styles:
        print ( use + '()' )
        eval(use + '()')
