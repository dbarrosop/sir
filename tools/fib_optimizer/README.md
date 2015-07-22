Required variables
------------------

    base_url = 'http://127.0.0.1:5000/api/v1.0'
    configuration = {
        lem_prefixes = '24',
        max_lem_prefixes = 200000,
        max_lpm_prefixes = 16000,
        age = 168,
    }

    from pySIR.pySIR import pySIR
    import json

    sir = pySIR(base_url)
    sir.post_variables(
        name = 'fib_optimizer',
        content = json.dumps(configuration),
        category = 'apps',
      )
