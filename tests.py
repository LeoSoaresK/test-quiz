import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices_increments_id():
    question = Question(title='q1')
    c1 = question.add_choice('choice 1')
    c2 = question.add_choice('choice 2')
    assert c1.id == 1
    assert c2.id == 2
    assert len(question.choices) == 2

def test_remove_choice_by_id():
    question = Question(title='q1')
    c1 = question.add_choice('choice 1')
    question.remove_choice_by_id(c1.id)
    assert len(question.choices) == 0

def test_remove_choice_invalid_id_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception, match="Invalid choice id 999"):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices_updates_status():
    question = Question(title='q1')
    c1 = question.add_choice('wrong')
    question.set_correct_choices([c1.id])
    assert c1.is_correct is True

def test_correct_selected_choices_returns_only_correct_ones():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('correct', is_correct=True)
    c2 = question.add_choice('wrong', is_correct=False)
    
    result = question.correct_selected_choices([c1.id, c2.id])
    assert c1.id in result
    assert c2.id not in result

def test_correct_selected_choices_exceeding_max_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([c1.id, c2.id])

def test_choice_text_empty_raises_exception():
    question = Question(title='q1')
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice("")

def test_choice_text_too_long_raises_exception():
    question = Question(title='q1')
    long_text = "a" * 101
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice(long_text)

def test_question_points_out_of_range_raises_exception():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=101)

@pytest.fixture
def question_with_choices():
    """Fixture que retorna uma questão configurada com 3 opções."""
    question = Question(title='Qual a capital de Minas Gerais?', points=10, max_selections=1)
    question.add_choice('São Paulo', is_correct=False)
    question.add_choice('Belo Horizonte', is_correct=True)
    question.add_choice('Rio de Janeiro', is_correct=False)
    return question

def test_fixture_question_title(question_with_choices):
    """Testa se a fixture carregou o título corretamente."""
    assert question_with_choices.title == 'Qual a capital de Minas Gerais?'

def test_fixture_correct_answer(question_with_choices):
    """Testa a correção usando a estrutura da fixture."""
    # O ID da segunda opção (Belo Horizonte) deve ser 2
    correct_id = 2 
    result = question_with_choices.correct_selected_choices([correct_id])
    assert len(result) == 1
    assert result[0] == correct_id

def test_fixture_points_calculation(question_with_choices):
    """Testa se os pontos da questão da fixture estão corretos."""
    assert question_with_choices.points == 10