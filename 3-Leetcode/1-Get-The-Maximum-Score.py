def max_sum(nums1, nums2):
    # Appending max values at end to minimise extra while loops while iterating
	nums1.append(100000000)
	nums2.append(100000000)

	length1 = len(nums1)
	length2 = len(nums2)

	index1 = 0
	index2 = 0
	max1 = 0
	max2 = 0

	while index1 < length1 or index2 < length2:
		if nums1[index1] < nums2[index2]:
			max1 += nums1[index1]
			index1 += 1
		elif nums1[index1] > nums2[index2]:
			max2 += nums2[index2]
			index2 += 1
		else:
			max1 = max(max1, max2) + nums1[index1]
			max2 = max1
			index1 += 1
			index2 += 1

	return (max1 - 100000000) % (1000000007)

nums1 = list(map(int, input().split()))
nums2 = list(map(int, input().split()))
print(max_sum(nums1, nums2))

