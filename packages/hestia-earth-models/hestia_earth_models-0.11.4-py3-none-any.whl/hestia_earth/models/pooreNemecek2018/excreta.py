from hestia_earth.schema import ProductStatsDefinition, TermTermType
from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.property import _get_nitrogen_content
from hestia_earth.models.utils.product import _new_product, animal_produced
from hestia_earth.models.utils.input import get_feed_nitrogen
from hestia_earth.models.utils.term import get_excreta_terms
from . import MODEL


def _product(value: float, excreta: str):
    logger.info('model=%s, term=%s, value=%s', MODEL, excreta, value)
    product = _new_product(excreta, MODEL)
    product['value'] = [value]
    product['statsDefinition'] = ProductStatsDefinition.MODELLED.value
    return product


def _run(product: dict, excreta: str, inputs_n: float, products_n: float, nitrogen_content: float, liveAquatic: bool):
    value = 3.31 * nitrogen_content / 100 * list_sum(product.get('value')) if liveAquatic and nitrogen_content \
        else inputs_n - products_n
    return [_product(value, excreta)]


def _no_excreta_term(products: list):
    term_ids = get_excreta_terms()
    return all([not find_term_match(products, term) for term in term_ids])


def _get_excreta_term(product: dict):
    term_id = product.get('term', {}).get('@id')
    term_type = product.get('term', {}).get('termType')
    lookup = download_lookup(f"{term_type}.csv", True)
    return get_table_value(lookup, 'termid', term_id, 'excreta')


def _should_run(cycle: dict):
    primary_prod = find_primary_product(cycle) or {}
    excreta = _get_excreta_term(primary_prod)
    dc = cycle.get('dataCompleteness', {})
    is_complete = dc.get('animalFeed', False) and dc.get('products', False)
    inputs = cycle.get('inputs', [])
    inputs_n = get_feed_nitrogen(inputs)
    products = cycle.get('products', [])
    products_n = animal_produced(products) / 100
    no_excreta = _no_excreta_term(products)

    # if animal feed is not complete, we can still run the model for `liveAquaticSpecies`
    product_value = list_sum(primary_prod.get('value', [0]))
    is_liveAquaticSpecies = not dc.get('animalFeed', False) and \
        product_value > 0 and \
        primary_prod.get('term', {}).get('termType') == TermTermType.LIVEAQUATICSPECIES.value
    nitrogen_content = _get_nitrogen_content(primary_prod)

    debugRequirements(model=MODEL, term=excreta,
                      is_complete=is_complete,
                      inputs_n=inputs_n,
                      products_n=products_n,
                      no_excreta=no_excreta,
                      is_liveAquaticSpecies=is_liveAquaticSpecies,
                      product_value=product_value,
                      nitrogen_content=nitrogen_content)

    should_run = excreta is not None and no_excreta and (
        all([is_liveAquaticSpecies, nitrogen_content]) or
        all([is_complete, inputs_n, products_n])
    )
    logger.info('model=%s, term=%s, should_run=%s', MODEL, excreta, should_run)
    return should_run, primary_prod, excreta, inputs_n, products_n, nitrogen_content, is_liveAquaticSpecies


def run(cycle: dict):
    should_run, product, excreta, inputs_n, products_n, nitrogen_content, is_liveAquaticSpecies = _should_run(cycle)
    return _run(product, excreta, inputs_n, products_n, nitrogen_content, is_liveAquaticSpecies) if should_run else []
