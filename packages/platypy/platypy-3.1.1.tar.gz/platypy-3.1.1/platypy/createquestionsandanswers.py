def question(question, option_1, option_2, option_3, option_4, answer, op_quantity):
    print("""{}
                {}    {}
                {}    {}""".format(question,option_1, option_2, option_3, option_4))
    ans = input("Write the correct option number[{}]: ".format(op_quantity))
    if ans == answer:
        print("Right answer!")
    else:
        print("wrong answer")

def createquiz(question1, question2, question3, question4, question5, options1, options2, options3, options4, options5, answer1, answer2, answer3, answer4, answer5, op_quantity1, op_quantity2, op_quantity3, op_quantity4, op_quantity5):
    def question_1(question1, option, answer, op_quantity):
        print("""{}
                {}    
                """.format(question1,option))
        ans = input("Write the correct option number[{}]: ".format(op_quantity))
        if ans == answer:
            print("Right answer!")
        else:
            print("wrong answer")
        global options_1
        options_1 = option
    def question_2(question2, options, answer, op_quantity):
        print("""{}
                {}""".format(question2,options))
        ans = input("Write the correct option number[{}]: ".format(op_quantity))
        if ans == answer:
            print("Right answer!")
        else:
            print("wrong answer")
        global options_2
        options_2 = options1
    def question_3(question3, option, answer, op_quantity):
        print("""{}
                {}
                """.format(question3, option))
        ans = input("Write the correct option number[{}]: ".format(op_quantity))
        if ans == answer:
            print("Right answer!")
        else:
            print("wrong answer")
        global options_3
        options_3 = option
    def question_4(question4, option, answer, op_quantity):
        print("""{}
                {}    
                """.format(question4,option))
        ans = input("Write the correct option number[{}]: ".format(op_quantity))
        if ans == answer:
            print("Right answer!")
        else:
            print("wrong answer")
        global options_4
        options_4 = option
    def question_5(question5, option, answer, op_quantity):
        print("""{}
                {}    
                """.format(question5,option))
        ans = input("Write the correct option number[{}]: ".format(op_quantity))
        if ans == answer:
            print("Right answer!")
        else:
            print("wrong answer")
        global options_5
        options_5 = option
    question_1(question1, options1, answer1, op_quantity1)
    question_2(question2, options2, answer2, op_quantity2)
    question_3(question3, options3, answer3, op_quantity3)
    question_4(question4, options4, answer4, op_quantity4)
    question_5(question5, options5, answer5, op_quantity5)
