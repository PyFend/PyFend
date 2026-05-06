from datetime import datetime

from pyfend.tools.hashprobe.utils import word_list


def test_create_smart_wordlist_data_builds_expected_variations() -> None:
    words = word_list.create_smart_wordlist_data(
        name="John Doe",
        nickname="JD",
        birth=datetime(2000, 1, 2),
        extra="admin,root",
    )

    assert "John" in words
    assert "john" in words
    assert "JohnDoe" in words
    assert "johndoe" in words
    assert "JD123" in words
    assert "admin2025" in words
    assert "2000John" in words or "John2000" in words
    assert len(words) == len(set(words))


def test_generate_smart_wordlist_writes_output_file(
    monkeypatch, tmp_path
) -> None:
    output_path = tmp_path / "additional.txt"
    monkeypatch.setattr(word_list, "ADDITIONAL_FILE", output_path)

    word_list.generate_smart_wordlist(
        {
            "name": "John Doe",
            "nickname": "JD",
            "birth": datetime(2000, 1, 2),
            "extra": "admin,root",
        }
    )

    assert output_path.exists()
    contents = output_path.read_text(encoding="utf-8").splitlines()
    assert "John" in contents
    assert "john" in contents
    assert "JohnDoe" in contents
    assert "johndoe" in contents
    assert "JD123" in contents
    assert "admin2025" in contents
    assert "2000John" in contents or "John2000" in contents
