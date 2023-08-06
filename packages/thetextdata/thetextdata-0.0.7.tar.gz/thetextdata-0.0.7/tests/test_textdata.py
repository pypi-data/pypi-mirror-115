# coding: utf-8

from unittest.mock import patch
import pytest
from thetextdata.textdata import embed, TextItem, TextData
from unittest.mock import Mock

from veriservice import veriservice_pb2 as pb


def test_embed():
    vector = embed("Apple.")
    assert len(vector) == 512


def test_text_item():
    info = "{id:'id0'}"
    text = "Who let the Dogs out? Who? Who?"
    item = TextItem(info=info, text=text)
    item.calculate_texts()
    texts = item.get_texts()
    texts.sort()
    assert 2 == len(texts)
    assert "Who let the Dogs out?" == texts[0]
    assert "Who?" == texts[1]

    item.add_text("Minor Addition.")
    item.calculate_texts()
    texts = item.get_texts()
    texts.sort()
    assert 3 == len(texts)
    assert "Minor Addition." == texts[0]
    assert "Who let the Dogs out?" == texts[1]
    assert "Who?" == texts[2]

    count = 0
    for entry in item.get_entries():
        assert entry["group_label"] == info
        assert len(entry["feature"]) == 512
        count = count + 1

    assert 3 == count

def test_text_item_increase_split_threshold_min():
    info = "{id:'id1'}"
    text = "Who let the Dogs out? Who? Who?"
    item = TextItem(info=info, text=text, split_threshold_min=100)
    item.calculate_texts()
    texts = item.get_texts()
    texts.sort()
    assert len(texts) == 1
    assert text == texts[0]


def test_text_data_insert():
    veri_client_mock = Mock()
    veri_client_mock.insert.return_value = None
    text_data = TextData(veri_client_mock)
    info = "{id:'id0'}"
    text = "Who let the Dogs out? Who? Who?"
    item = TextItem(info=info, text=text)
    text_data.insert(item)
    veri_client_mock.insert.assert_called()


def test_text_data_item_search():
    veri_client_mock = Mock()
    expected_result = [
        pb.ScoredDatum(
            score=0.9,
            datum=pb.Datum(
                key=pb.DatumKey(
                    feature=embed("text1").tolist(),
                    groupLabel="{\"id\":\"id1\"}".encode(),
                    size1=1,
                    size2=0,
                    dim1=512,
                    dim2=0,
                ),
                value=pb.DatumValue(
                    version=None,
                    label="{\"text\":\"text1\"}".encode(),
                ),
            )
        )

    ]
    veri_client_mock.search.return_value = expected_result
    text_data = TextData(veri_client_mock)
    text = "Who let the Dogs out? Who? Who?"
    result = text_data.search(text)
    veri_client_mock.search.assert_called()
    assert len(result) == 1


def test_text_item_reduce():
    info = "{id:'id0'}"
    input_texts = ["A corona virus title",
            "Corona vaccine.",
            "Another virus title.",
            "Corona is spreding.",
            "Vaccines are important.",
            "We are late on vaccines.",
            "There is a new Match.",
            "Goool, we are gonna win.",
            "Goalkeeper is nowhere to be found.",
            "Another coronavirus thing.",
            "Vaccines are again important.",
            "Football is nice."]
    item = TextItem(info=info, text=input_texts)
    item.calculate_texts()
    item.reduce_texts(2, 5, 10, 12)
    texts = item.get_texts()
    texts.sort()
    assert 3 == len(texts)
    assert texts == ['Another coronavirus thing.', 'Football is nice.', 'Vaccines are important.']