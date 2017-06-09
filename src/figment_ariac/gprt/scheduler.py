#!/usr/bin/env python
import rospy
import order_utils
import execution


class PickPiece:

	def __init__(self, origin, world_position, world_orientation):
		self.origin 			= origin #binX, belt or agvN
		self.world_position 	= world_position
		self.world_orientation 	= world_orientation

class KitPlan:

	def __init__(self, kit, dest_tray_id, list_part_plan):
		self.kit = kit
		self.dest_tray_id = dest_tray_id
		self.list_part_plan = list_part_plan
		self.planning_score = -1

	def compute_score(self):
		score = 0
		for partPlan in list_part_plan:
			score += partPlan.compute_score()
		return score	

class PartPlan:

	def __init__(self, part, dest_tray_id, pick_piece):
		self.part = part
		self.dest_tray_id = dest_tray_id
		self.pick_piece = pick_piece
		self.planning_score = -1

	def compute_score(self):
		pass


class Scheduler:



	def __init__(self, competition):
		self.order_list = []
		self.finished = False
		self.competition = competition


	def append_order(self, order):
		pass

	def isFinished(self):
		return self.finished

	def setFinished(status):
		self.finished = status

	def execute(self):
		while not self.isFinished():
			part_plan = self.get_next_part_plan()
			if part_plan is None:
				rospy.loginfo("[Scheduler] No possible Part Plan yet...")
				rospy.loginfo("[Scheduler] Sleeping...")
				rospy.sleep(1)
			else:
				execute_part = execution.ExecutePart(part_plan)
				status = execute_part.execute()

	#Get non finished high priority order
	def get_non_fin_hp_order(self):
		len_order_list = len(self.order_list)		
		idx_high_priority = len_order_list-1 #Last means high priority

		while idx_high_priority > 0:
			working_order = order_list[idx_high_priority] 
			#Not sure yet what to do for other states (HALTED, ERROR)
			if(working_order.get_status() is not order_utils.Status.FINISHED): 
				return working_order

	def get_next_part_plan(self):
		len_order_list = len(self.order_list)

		if(len_order_list == 0):
			rospy.loginfo("[Scheduler] No Orders yet...")	
			return

		working_order = self.get_non_fin_hp_order()
		if(working_order is None):
			rospy.loginfo("[Scheduler] There are no unfinished orders")	
			return

		working_kit = self.get_frs_non_fin_kit_from_ord(working_order)
		if(working_kit is None):
			rospy.logerr("[Scheduler] There are no unfinished kit but the order is not finished")
			rospy.logerr(working_order.get_full_repr())	
			return

		working_part = self.get_frs_non_fin_part_from_kit(working_kit)
		if(working_part is None):
			rospy.logerr("[Scheduler] There are no unfinished part but the kit is not finished")
			rospy.logerr(working_order.get_full_repr())	
			return

		return working_part

	#Get first non finished part from kit
	def get_frs_non_fin_part_from_kit(self, kit):
		for part in kits.parts:
			#Not sure yet what to do for other states (HALTED, ERROR)
			if(part.get_status() is not order_utils.Status.FINISHED):
				return part
		


	#Get first non finished part from kit
	def get_frs_non_fin_kit_from_ord(self, order):
		for kit in order.kits:
			#Not sure yet what to do for other states (HALTED, ERROR)
			if(kit.get_status() is not order_utils.Status.FINISHED):
				return kit





