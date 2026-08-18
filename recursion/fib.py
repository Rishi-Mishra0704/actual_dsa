def fib(n) :
        memo = {}
        def helper(n):
            if n <= 1:
                return n
            
            if n in memo:
                return memo[n]
            
            result = helper(n-1)+helper(n-2)
            memo[n] = result
            return result

        return helper(n)

