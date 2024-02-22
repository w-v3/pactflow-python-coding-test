from pypacter.reviewer import Reviewer


def test_reviewer_python() -> None:
    reviewer = Reviewer()

    recommendations = reviewer.invoke({
        "code": '''
        def add(a, b):
            """
            Sum two numbers
            """
            return a + b
        '''
    }).recommendations
    assert len(recommendations) == 0

    recommendations = reviewer.invoke({
        "code": '''
        def add(a, b, c):
            """
            Sum two numbers
            """
            return a + b
        '''
    }).recommendations
    assert len(recommendations) > 0
