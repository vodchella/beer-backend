from pkg.utils.dynamic_import import dynamic_import


dynamic_import('./pkg/rest/routes/v1',
               'pkg.rest.routes.v1',
               '... loading routes:',
               '...... %s route loaded')
