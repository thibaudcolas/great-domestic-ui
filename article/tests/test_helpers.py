from unittest.mock import patch, call

from directory_constants.constants import exred_articles
import pytest
import requests

from article import articles, helpers, structure
from core.tests.helpers import create_response


@pytest.fixture
def articles_read():
    return [
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '1',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.CONSIDER_HOW_PAID
        },
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '2',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.INVOICE_CURRENCY_AND_CONTENTS
        },
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '3',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.PLAN_THE_LOGISTICS
        }
    ]


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_calls_api(
        mock_create_article_read,
        mock_retrieve_article_read,
        sso_request,
        sso_user
):
    mock_create_article_read.return_value = create_response(200)

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    manager.persist_article(article_uuid='123')

    assert mock_create_article_read.call_count == 1
    assert mock_create_article_read.call_args == call(
        article_uuid='123',
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_handle_exceptions(
        mock_create_article_read,
        mock_retrieve_article_read,
        sso_request,
):
    mock_create_article_read.return_value = create_response(400)
    manager = helpers.DatabaseArticlesReadManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.persist_article(article_uuid='123')


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_article_read_count(
        mock_retrieve_article_read,
        sso_request,
        articles_read
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=articles_read
    )
    group_key = structure.GUIDANCE_GETTING_PAID_ARTICLES.name
    manager = helpers.DatabaseArticlesReadManager(sso_request)
    count = manager.article_read_count(group_key)
    articles_uuids = manager.read_articles_keys_in_group(group_key)
    assert sorted(list(articles_uuids)) == [
        exred_articles.CONSIDER_HOW_PAID,
        exred_articles.INVOICE_CURRENCY_AND_CONTENTS,
    ]
    assert count == 2


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_get_group_read_progress(
    mock_retrieve_article_read, sso_request, articles_read
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=articles_read
    )

    manager = helpers.ArticleReadManager(sso_request)
    actual = manager.get_group_read_progress()
    assert actual == {
        'all': {'read': 3, 'total': 45},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 2, 'total': 5},
        'market_research': {'read': 0, 'total': 5},
        'operations_and_compliance': {'read': 1, 'total': 10},
        'persona_new': {'read': 2, 'total': 18},
        'persona_occasional': {'read': 2, 'total': 38},
        'persona_regular': {'read': 0, 'total': 18},
        'custom_persona_new': {'read': 2, 'total': 18},
        'custom_persona_occasional': {'read': 2, 'total': 38},
        'custom_persona_regular': {'read': 0, 'total': 18},
    }


def test_session_get_group_read_progress(anon_request, articles_read):

    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = [i['article_uuid'] for i in articles_read]

    manager = helpers.ArticleReadManager(anon_request)
    actual = manager.get_group_read_progress()

    assert actual == {
        'all': {'read': 3, 'total': 45},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 2, 'total': 5},
        'market_research': {'read': 0, 'total': 5},
        'operations_and_compliance': {'read': 1, 'total': 10},
        'persona_new': {'read': 2, 'total': 18},
        'persona_occasional': {'read': 2, 'total': 38},
        'persona_regular': {'read': 0, 'total': 18},
        'custom_persona_new': {'read': 2, 'total': 18},
        'custom_persona_occasional': {'read': 2, 'total': 38},
        'custom_persona_regular': {'read': 0, 'total': 18},
    }


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_remaining_reading_time_in_group(
    mock_retrieve_article_read, sso_request, articles_read
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=articles_read
    )

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    time_left = manager.remaining_reading_time_in_group(
        structure.PERSONA_OCCASIONAL_ARTICLES.name
    )

    assert time_left == 5395


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_read_api_call(
    mock_retrieve_article_read, sso_request, sso_user,
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=[
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '1',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '123'
            },
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '2',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '345'
            }
        ]
    )

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    articles = manager.retrieve_article_uuids()

    assert articles == {'123', '345'}
    assert mock_retrieve_article_read.call_count == 2
    assert mock_retrieve_article_read.call_args == call(
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.create_article_read')
@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_update_from_session(
        mock_retrieve_article_read,
        mock_create_article_read,
        sso_request,
        sso_user,
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=[
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '1',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '123'
            },
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '2',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '345'
            }
        ]
    )

    key = helpers.SessionArticlesReadManager.SESSION_KEY
    sso_request.session[key] = {'678', '123'}
    helpers.DatabaseArticlesReadManager(sso_request)

    assert mock_create_article_read.call_count == 1
    assert mock_create_article_read.call_args == call(
        article_uuid='678', sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_read_handle_exceptions(
    mock_retrieve_article_read, sso_request,
):
    mock_retrieve_article_read.return_value = create_response(400)

    with pytest.raises(requests.HTTPError):
        manager = helpers.DatabaseArticlesReadManager(sso_request)
        manager.retrieve_article_uuids()


def test_session_article_manager_stores_in_session_no_existing_articles(
        anon_request
):
    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(article_uuid='123')

    assert anon_request.session[manager.SESSION_KEY] == ['123']


def test_session_article_manager_stores_in_session_existing_articles(
        anon_request
):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(article_uuid='345')

    assert anon_request.session[manager.SESSION_KEY] == ['123', '345']


def test_session_article_manager_retrieves_from_session(anon_request):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesReadManager(anon_request)
    answers = manager.retrieve_article_uuids()

    assert answers == {'123'}


def test_session_article_read_count(anon_request):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    articles_uuids = [
        exred_articles.PLAN_THE_LOGISTICS,
        exred_articles.USE_FREIGHT_FORWARDER,
        exred_articles.CONSIDER_HOW_PAID
    ]
    anon_request.session[key] = articles_uuids
    assert anon_request.session[key] == articles_uuids

    group_key = structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES.name
    manager = helpers.SessionArticlesReadManager(anon_request)
    returned_articles_uuids = manager.read_articles_keys_in_group(group_key)
    count = manager.article_read_count(group_key)
    expected_articles_uuids = sorted([
        exred_articles.PLAN_THE_LOGISTICS,
        exred_articles.USE_FREIGHT_FORWARDER,
    ])
    assert sorted(list(returned_articles_uuids)) == expected_articles_uuids
    assert count == 2


def test_session_remaining_reading_time_in_group(anon_request):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = [
        exred_articles.DEFINE_MARKET_POTENTIAL,
        exred_articles.DO_FIELD_RESEARCH,
        exred_articles.ANALYSE_THE_COMPETITION
    ]
    assert anon_request.session[key] == [
        exred_articles.DEFINE_MARKET_POTENTIAL,
        exred_articles.DO_FIELD_RESEARCH,
        exred_articles.ANALYSE_THE_COMPETITION
    ]

    manager = helpers.SessionArticlesReadManager(anon_request)
    time_left = manager.remaining_reading_time_in_group(
        structure.PERSONA_OCCASIONAL_ARTICLES.name
    )

    assert time_left == 5032


def test_filter_lines():
    lines = ['foo', '\n', 'bar']
    assert list(helpers.filter_lines(lines)) == ['foo', 'bar']


def test_lines_from_html():
    html = '<p>foo</p><p>bar</p>'
    assert helpers.lines_list_from_html(html) == ['foo', 'bar']


def test_count_average_word_number():
    lines_list = [
        'Lorem Ipsum is simply dummy text of the printing and typesetting',
        'Lorem Ipsum has been the industry\'s standard dummy '
    ]
    assert helpers.count_average_word_number_in_lines_list(
        lines_list
    ) == 23.0


def test_time_to_read_in_seconds():
    article = articles.INVOICE_CURRENCY_AND_CONTENTS
    assert helpers.time_to_read_in_seconds(
        article
    ) == 279


def test_total_time_to_read_multiple_articles():
    articles_list = [
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.PLAN_THE_LOGISTICS
    ]
    assert helpers.total_time_to_read_multiple_articles(
        articles_list
    ) == 318
