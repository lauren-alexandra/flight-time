"""
Description: An algorithm that gives you the smallest edit distance between any two words.
"""

def main():

    memo = dict()

    def find_edit_dist(word1, word2, word1_len, word2_len):
    
        # Base cases
        # if first word is empty, need to insert all letters from second word
        if word1_len == 0:
            return word2_len
    
        # if second word is empty, need to insert all letters from first word
        if word2_len == 0:
            return word1_len
    
        # use cached solution to a subproblem
        key = word1_len, word2_len
        if key in memo: return memo[key]
            
        # if letters the same, continue to find the remaining edits
        if word1[word1_len - 1] == word2[word2_len - 1]:
            return find_edit_dist(word1, word2, word1_len - 1, word2_len - 1)

        # General case
        # take the minimum of the min cost for insert, delete, and copy operations 
        # store the result of subproblem in memo dictionary 
        memo[key] = 1 + min(find_edit_dist(word1, word2, word1_len, word2_len - 1), # insertion
                            find_edit_dist(word1, word2, word1_len - 1, word2_len), # deletion
                            find_edit_dist(word1, word2, word1_len - 1, word2_len - 1)) # copy
        return memo[key]

    words = input("\nPlease enter two words separated by a comma: ")
    words = words.split(',')
    words = [word.strip() for word in words]
    w1, w2 = words[0], words[1]
    print(f"\nEdit distance: {find_edit_dist(w1, w2, len(w1), len(w2))}")

if __name__ == "__main__":
    main()
