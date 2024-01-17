def best_rotation(nums):
	n = len(nums)
	prefix = [0]*(n)

	for index in range(n):
		prefix[(index + 1)%n] += 1
		prefix[(index - nums[index] + 1)%n] -= 1

	max_value = prefix[0]
	max_i = 0
	for i in range(1,n):
		prefix[i] = prefix[i] + prefix[i-1]
		if max_value < prefix[i]:
			max_value = prefix[i]
			max_i = i
	return max_i

nums = list(map(int, input().split()))
print(best_rotation(nums))
