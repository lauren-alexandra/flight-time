"""
Description: The program finds the smallest edit distance between any two words. 
A letter may be copied at the cost of 5, deleted at the cost of 20, or inserted
at the cost of 20.
"""

from collections import Counter

def main():

    def edit_dist(str1, str2):
        word1_len, word2_len = len(str1), len(str2)
        goal_word = Counter(str2)
        memo = {"total": 0}

        def checkCopy(letter):
            if goal_word[letter] != 0: return 25
            else: return 50 # negates the copy value in min

        def find_cost(i): # i is the index of a subproblem 
            combined_op_cost = 40 # insert new 20, del old 20
            highest_op_cost = 20

            # Base case: (i == word1_len or i == word2_len) 
            if i == word1_len or i == word2_len:
                diff = word1_len - word2_len
                remaining = abs(diff) * highest_op_cost 
                memo['total'] = memo['total'] + remaining       
                return None

            # edge case: str1 empty
            if word1_len == 0: 
                memo['total'] = len(str2) * highest_op_cost
                return None

            # General case: (0 <= i < word1_len and 0 <= i < word2_len)
            letter = str1[i]
            # check if same letter at same index
            if (letter == str2[i]): 
                return find_cost(i+1)
            elif letter in memo.keys(): 
                memo['total'] = memo['total'] + memo[letter]
            else:          
                min_edit = min(checkCopy(letter), combined_op_cost) 
                # store the result of subproblem in memo dictionary 
                memo[letter] = min_edit
                memo['total'] = memo['total'] + min_edit

            return find_cost(i+1) 
            
        # Goal: find cost
        find_cost(0)
        
        print(f"\nTotal cost: {memo['total']}")
        return memo['total']

    words = input("\nPlease enter two words separated by a comma: ")
    words = words.split(',')
    words = [word.strip() for word in words]
    edit_dist(words[0], words[1])


if __name__ == "__main__":
    main()
