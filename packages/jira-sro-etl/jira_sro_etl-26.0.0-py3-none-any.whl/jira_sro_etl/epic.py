import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity
from tqdm import tqdm

from sro_db.application import factories
from sro_db.model import factories as factories_model
from .conversor import factories as factories_conversor

from datetime import datetime

from .scrum_project import scrum_project as etl_scrum_project
from .team_member import team_member as etl_team_member
from .sprint import sprint as etl_sprint

""" An epic """
class epic(BaseEntity):
	"""
	Class responsible for handle epics from jira
	"""
	def create(self, data: dict, jira_issue: object = None, jira_project: object = None) -> object:
		"""Create an Epic on Sro's database (if this epic already exists, do nothing)

		Args:
			data (dict): Dict with jira issue information (issue_id = data['content']['all']['issue']['id'])
			and project information (project_id = data['content']['all']['issue']['fields']['project']['id'])
			jira_issue (object, optional): Issue from Jira
			jira_project (object, optional): Project from Jira

		Returns:
			object: Epic created by a sro_db's factory
		"""
		try:
			logging.info("Creating Epic")

			if jira_issue is None:
				# check if exists in database
				issue_id = data['content']['all']['issue']['id']
				epic_application = factories.EpicFactory()
				ontology_Epic = epic_application.retrive_by_external_uuid(issue_id)
				if (ontology_Epic != None):
					logging.info("Epic already exist in database")
					return
				else:
					issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
					jira_issue = issue_apl.find_by_id(issue_id)
			else:
				# check if exists in database
				issue_id = jira_issue.id
				epic_application = factories.EpicFactory()
				ontology_Epic = epic_application.retrive_by_external_uuid(issue_id)
				if (ontology_Epic != None):
					logging.info("Epic already exist in database")
					return

			if jira_project is None:
				project_id = data['content']['all']['issue']['fields']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)

			self.conversor = factories_conversor.ConversorEpicFactory(organization = self.organization, data = self.data)
			epic = self.conversor.convert(
				etl_scrum_project, etl_team_member,
				jira_issue, jira_project)
			
			epic_application = factories.EpicFactory()
			epic = epic_application.create(epic)
			self.create_application_reference('issue', epic, jira_issue.id, jira_issue.self)
			
			# Assignee
			print('assignee')
			assignee = jira_issue.raw.get("fields").get("assignee")
			if assignee != None:
				assignee_id = assignee.get('accountId')
				team_member_application = factories.TeamMemberFactory()
				ontology_team_member = team_member_application.retrive_by_external_id_and_project_name(assignee_id, 
				jira_project.name)
				if ontology_team_member is None:
					team_member = etl_team_member()
					team_member.config(self.data)
					data_to_create = {'accountId': assignee_id}
					ontology_team_member = team_member.create(data_to_create, None, jira_project)
				association_development_task = factories_model.AssociationUserStorySprintTeammemberFactory()
				association_development_task.date = datetime.datetime.now()
				association_development_task.activate = True
				association_development_task.user_story_id = epic.id
				association_development_task.team_member_id = ontology_team_member.id

				ontology_association_development_task_application = factories.AssociationUserStorySprintTeammemberFactory()
				ontology_association_development_task_application.create(association_development_task)


			print('Atomic_user_story_sprint_backlog')
			# print('passou o sprint')
			# Sprint_backlog association_sprint_backlog_scrum_development_activity_table
			# sprints = jira_issue.raw.get("fields").get("customfield_10018") # wize
			# sprint_name = jira_issue.raw.get("fields").get("customfield_10020")[-1].get('name') # ledzepplin
			# sprint_id = jira_issue.raw.get("fields").get("customfield_10020")[-1].get('id') # ledzepplin
			sprint_name = jira_issue.raw.get("fields").get("customfield_10018")[-1].get('name')
			sprint_id = jira_issue.raw.get("fields").get("customfield_10018")[-1].get('id')
			if sprint_name != None:
				sprint_backlog_application = factories.SprintBacklogFactory()
				ontology_sprint_backlog = sprint_backlog_application.retrive_by_name_and_project_name(sprint_name, jira_project.name)
				if ontology_sprint_backlog is None:
					sprint = etl_sprint()
					sprint.config(self.data, 'sprint')
					data_to_create = {'content':{'all':{'sprint':{'id': sprint_id}}}}
					ontology_sprint_backlog = sprint.create(data_to_create, None, jira_project)
				association = factories_model.AssociationAtomicUserStorySprintBacklogFactory()
				association.date = datetime.datetime.now()
				association.activate = True
				association.user_story_id = epic.id
				association.sprint_backlog_id = ontology_sprint_backlog.id

				ontology_association = factories.AssociationAtomicUserStorySprintBacklogFactory()
				ontology_association.create(association)

			logging.info("Epic created")

			self.insert_one_on_mongo_db(jira_issue.raw, 'issue')

			return epic

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Epic")

	def update(self, data: dict) -> object:
		"""Update an Epic on Sro's database

		Args:
			data (dict): Dict with jira issue information (issue_id = data['content']['all']['issue']['id'])

		Returns:
			object: Epic created by a sro_db's factory
		"""
		try:
			logging.info("Updating Epic")
			
			issue_id = data['content']['all']['issue']['id']
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			jira_issue = issue_apl.find_by_id(issue_id)

			project_id = data['content']['all']['issue']['fields']['project']['id']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_id(project_id)

			epic_application = factories.EpicFactory()

			self.conversor = factories_conversor.ConversorEpicFactory(organization = self.organization, data = self.data)
			epic = self.conversor.convert(
				etl_scrum_project, etl_team_member,
				jira_issue, jira_project,
				epic_application.retrive_by_external_uuid(issue_id))
			
			epic_application.update(epic)

			# Assignee
			assignee = jira_issue.raw.get("fields").get("assignee")
			if assignee != None:
				print('Tem assignee')
				assignee_id = assignee.get('accountId')
				team_member_application = factories.TeamMemberFactory()
				print(f'Assignee: {assignee_id}')
				print(f'Project name: {jira_project.name}')
				ontology_team_member = team_member_application.retrive_by_external_id_and_project_name(assignee_id, 
				jira_project.name)
				print(f"Ontology team member {ontology_team_member}")
				# exit()
				if ontology_team_member is None:
					team_member = etl_team_member()
					team_member.config(self.data)
					data_to_create = {'accountId': assignee_id}
					ontology_team_member = team_member.create(data_to_create, None, jira_project)
				
				print('Cria a associação')
				
				association = factories_model.AssociationUserStorySprintTeammemberFactory()
				association.date = datetime.datetime.now()
				association.activate = True
				association.user_story_id = atomic_user_story.id
				association.team_member_id = ontology_team_member.id

				print('Tenta update')

				ontology_association_application = factories.AssociationUserStorySprintTeammemberFactory()
				ontology_association_application.update(association)


			print('Atomic_user_story_sprint_backlog')
			# print('passou o sprint')
			# Sprint_backlog association_sprint_backlog_scrum_development_activity_table
			# sprints = jira_issue.raw.get("fields").get("customfield_10018") # wize
			sprint_name = jira_issue.raw.get("fields").get("customfield_10018")[-1].get('name')
			sprint_id = jira_issue.raw.get("fields").get("customfield_10018")[-1].get('id')
			# sprint_name = jira_issue.raw.get("fields").get("customfield_10020")[-1].get('name') # ledzepplin
			# sprint_id = jira_issue.raw.get("fields").get("customfield_10020")[-1].get('id') # ledzepplin
			if sprint_name != None:
				sprint_backlog_application = factories.SprintBacklogFactory()
				ontology_sprint_backlog = sprint_backlog_application.retrive_by_name_and_project_name(sprint_name, jira_project.name)
				if ontology_sprint_backlog is None:
					sprint = etl_sprint()
					sprint.config(self.data, 'sprint')
					data_to_create = {'content':{'all':{'sprint':{'id': sprint_id}}}}
					ontology_sprint_backlog = sprint.create(data_to_create, None, jira_project)
				association = factories_model.AssociationAtomicUserStorySprintBacklogFactory()
				association.date = datetime.datetime.now()
				association.activate = True
				association.user_story_id = atomic_user_story.id
				association.sprint_backlog_id = ontology_sprint_backlog.id

				ontology_association = factories.AssociationAtomicUserStorySprintBacklogFactory()
				ontology_association.update(association)

			logging.info("Epic updated")

			self.find_one_and_update_on_mongo_db('issue', jira_issue.raw, 'id', jira_issue.raw['id'])

			return epic

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Epic")	

	def delete(self, data):
		pass

	def do(self, data: dict) -> None:
		"""Retrieve epics from mongo and save them on sro's database

		Args:
			data (dict): With user, key and server to connect with jira
		"""
		try:
			logging.info("Epic")
			self.config(data)
			pprint ("Epic")
			
			mongo_collection_name = self.mongo_db.get_collection('issue')
			jira_epics = mongo_collection_name.find({"fields.issuetype.name":"Epic"})
			epic_list = []

			for jira_element in jira_epics:
				
				ontology_epic = factories_model.EpicFactory()
				
				self.fill_development_task(ontology_epic, jira_element)
				
				ontology_epic.product_backlog_id = jira_element['sro_db_product_backlog_id']
				
				epic_list.append(ontology_epic)
			epic_application = factories.EpicFactory()
			epic_list = epic_application.create_bulk (epic_list)

			self.create_application_reference_bulk(epic_list,'issue','id','self')

			#Salvando a relação entre team member e assigned da tarefa	e epic
			self.create_user_story_team_member(epic_list)

			#salvando sprint_backlog e epic
			self.create_user_story_spring_backlog(epic_list)
			
			#atualizando todos os IDs de epic
			for epic in epic_list:
				index_value = epic.jira_element['id']
				field_value = epic.id
				self.update_one_query("issue", "task_parent_id", str(index_value), "sro_db_task_parent_id",field_value)
				self.update_one_query("issue", "task_parent_id", str(index_value), "task_parent_type","epic")
			
			logging.info("Successfully done Epic")
			pprint("Successfully done Epic")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Epic")

	def update_by_time(self, data: dict, time: str):
		"""Retrieve epics from jira and save them on sro's database

		Args:
			data (dict): With user, key and server to connect with jira
			time (str): '1d' Will bring all epics created or updated on last 24h
		"""
		try:
			logging.info("Update Epic by time")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			epic_application = factories.EpicFactory()

			projects = project_apl.find_all()
			for project in tqdm(projects, desc='Epic'):
				epics = issue_apl.find_epic_by_project(project.key, time)
				for jira_epic in epics:
					ontology_epic = epic_application.retrive_by_external_uuid(jira_epic.id)
					if ontology_epic is not None:
						epic = self.conversor.epic(
							etl_scrum_project, etl_team_member,
							jira_epic, project,
							ontology_epic)
						epic_application.update(epic)
					else:
						self.create(None, jira_epic, project)

			logging.info("Successfully updated Epic by time")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Epic by time")
