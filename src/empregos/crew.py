from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool
from empregos.tools.linkedin import LinkedInTool

@CrewBase
class RecruitmentCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ## agents ##
    
    @agent
    def analista_de_perfil(self) -> Agent:
        return Agent(
            config=self.agents_config['analista_de_perfil'],
            tools=[],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def pesquisador_de_oportunidades(self) -> Agent:
        return Agent(
            config=self.agents_config['pesquisador_de_oportunidades'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), LinkedInTool()],
            allow_delegation=False,
            verbose=True,
            max_iter=1
        )

    @agent
    def criador_de_curriculos(self) -> Agent:
        return Agent(
            config=self.agents_config['criador_de_curriculos'],
            tools=[],
            allow_delegation=False,
            verbose=True
        )

    ## tasks ##

    @task
    def analisar_perfil_do_candidato_task(self) -> Task:
        return Task(
            config=self.tasks_config['analisar_perfil_do_candidato_task'],
            agent=self.analista_de_perfil()
        )

    @task
    def procurar_por_vagas_task(self) -> Task:
        return Task(
            config=self.tasks_config['procurar_por_vagas_task'],
            agent=self.pesquisador_de_oportunidades(),
            context=[self.analisar_perfil_do_candidato_task()]
        )

    @task
    def criar_curriculos_personalizados_task(self) -> Task:
        return Task(
            config=self.tasks_config['criar_curriculos_personalizados_task'],
            agent=self.criador_de_curriculos(),
            context=[self.procurar_por_vagas_task()],
            tools=[DirectoryReadTool(directory='D:/github/recruitment/outputs'), FileWriterTool()],
        )

    ## begin ##
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file="logs.txt"
        )
