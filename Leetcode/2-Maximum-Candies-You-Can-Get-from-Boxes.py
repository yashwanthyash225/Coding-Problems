def max_candies(status, candies, keys, contained_boxes, initial_boxes):
	total_candies = 0
	n_boxes = len(status)

	visited = []
	for _ in range(n_boxes):
		visited.append(False)
	for label in initial_boxes:
		visited[label] = True

	while True:
		flag = True
		box_list = []
		for box_label in initial_boxes:
			if status[box_label] == 1:
				flag = False
				total_candies += candies[box_label]
				for box in contained_boxes[box_label]:
					if visited[box] == False:
						box_list.append(box)
						visited[box] = True
				for key in keys[box_label]:
					status[key] = 1
			else:
				box_list.append(box_label)
		initial_boxes = box_list
		if flag:
			break

	return total_candies
