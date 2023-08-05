# coding=utf-8
import requests
import base64
import json

class GithubUtilsApi:
    '''
    GithubUtilsClass, created to let other scripts to automate DevOps HelpDesk Support
    '''
    def __init__(self, user, token, github_url="https://api.github.com", proxies={}, verify=True):
        '''
        Contructor
        :params user: string; user account at github (email)
        :params token: string; auth personal token with enough permission provided (or password)
        :params github_url: string; for GitHub Enterprise take in cosinderation the following pattern http(s)://[hostname]/api/v3/
        :params proxies: proxies
        '''
        self.github_url = github_url
        self.__user = user
        self.__token = token
        self.__auth = "Basic "+ str(base64.b64encode(str(self.__user+":"+token).encode('ascii')), "utf-8")
        self.proxies = proxies
        self.verify = verify
        self.github_url_graphql = f"{github_url}/api/graphql"

    def __request(self, type, url, data):
        '''
        Request Method with Auth Header required by Github
        '''
        headers = {
            'accept': 'application/vnd.github.v3+json',
            'Authorization': self.__auth
        }
        body = json.dumps(data)
        return requests.request(type, url, headers=headers, data=body, proxies=self.proxies, verify=self.verify)
    
    def __response_to_json(self,response):
        '''
        This method let you parse request body to JSON
        :param response: request response object
        :return: Array result
        '''
        result = []
        if(response.status_code >= 200 and response.status_code <= 201):
            result = json.loads(response.content)
        if ('errors' in result):
            print(f"There was an error in request: {str(response.content)}")
            result = []
        return result
        
    def organization_members_list(self, organization_name, per_page=30, page=1):
        '''
        This method let you list GH users in a organization
        According API docs: https://docs.github.com/en/rest/orgs/members#list-organization-members
        :param organization_name: string; name of the current organization created at github
        :param per_page: int; users per page
        :param page: int; page
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/orgs/" + organization_name + "/members" + query
        return self.__request("GET", url, params)

    def repository_org_create(self, organization_name=None, repository_name=None, visibility="private"):
        '''
        This method allows creating a repository in a defined Github organization
        According API docs: https://docs.github.com/en/rest/reference/repos#create-an-organization-repository
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param visibility: private, public or internal
        :return: request
        '''
        params = {}
        if repository_name:
            params['name'] = repository_name
        if visibility:
            params['visibility'] = visibility
        url = self.github_url + "/orgs/" + organization_name + "/repos"
        return self.__request("POST", url, params)

    def repository_grant_team(self, organization_name=None, repository_name=None, repository_owner=None, team_slug_name=None, team_permission='push'):
        '''
        This methows allows granting a Github Team in an specific repository.
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-repository-permissions 
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param repository_owner: string; organization/user owner
        :param team_slug_name: string; Github Team slug name
        :param team_permission: string; options available are -> pull, push, admin, maintain, triage
        :return: request
        '''
        params = {}
        if team_permission:
            params['permission'] = team_permission
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/repos/" + repository_owner + "/" + repository_name
        return self.__request("PUT", url, params)
    
    def organization_grant_user(self, organization_name=None, github_username=None):
        '''
        This methows allows granting a Github Team in an specific repository.
        According API docs: https://docs.github.com/en/rest/orgs/members
        :param organization_name: string; name of the current organization created at github
        :param github_username: string; Github Username
        :return: request
        '''

        params = {}
        if github_username:
            params['role'] = 'member'
        url = self.github_url + "/orgs/" + organization_name + "/memberships/" + github_username
        return self.__request("PUT", url, params)


    def team_create(self, organization_name=None, team_slug_name=None, team_privacy="closed"):
        '''
        This method allows creating a GitHub Team in a defined Github Organization
        According API docs: https://docs.github.com/en/rest/reference/teams#create-a-team
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param team_privacy: string; options available -> "secret" (only member) or "closed" all organizational members
        :return: request
        '''
        params = {}
        if team_slug_name:
            params['name'] = team_slug_name
        if team_privacy:
            params['privacy'] = team_privacy
        url = self.github_url + "/orgs/" + organization_name + "/teams"
        return self.__request("POST", url, params)

    def team_grant_user(self, organization_name=None, team_slug_name=None, github_username=None, team_role="member"):
        '''
        This method allows granting a user in a GitHub organization Team  
        According API docs: https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param github_username: string; Github Username
        :param team_role: values-> member or maintainer
        :return: request
        '''
        params = {}
        if team_role:
            params['role'] = team_role
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self.__request("PUT", url, params)

    def team_remove_user(self, organization_name=None, team_slug_name=None, github_username=None):
        '''
        This method allows removing a user in a GitHub organization Team  
        According API docs: https://docs.github.com/en/rest/reference/teams#remove-team-membership-for-a-user
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param github_username: string; Github Username
        :return: request
        '''
        params = {}
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/memberships/" + github_username
        return self.__request("DELETE", url, params)

    def team_list_users(self, organization_name=None, team_slug_name=None):
        '''
        This method allows list all user in a GitHub organization Team  
        According API docs: https://docs.github.com/en/rest/teams/members#list-team-members
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :return: request
        '''
        params = {}
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/members"
        return self.__request("GET", url, params)

    def team_discussion_create(self, organization_name=None, team_slug_name=None, discussion_title=None, private=False):
        '''
        This method creates a new discussion post on a team's page
        According API docs: https://docs.github.com/en/rest/teams/discussions#create-a-discussion
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param discussion_title: string; The discussion post's title.
        :param private: boolean; Private posts are only visible to team members, organization owners, and team maintainers. Public posts are visible to all members of the organization. Set to true to create a private post.
        :return: request
        '''
        body = {
            'title': discussion_title,
            'body': discussion_title,
            'private': private
        }
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions"
        return self.__request("POST", url, body)

    def team_discussion_search(self, organization_name=None, team_slug_name=None, discussion_title=None, create_if_not_exists=False, private=False):
        '''
        This method returns a discussion if exists, else None
        According API docs: https://docs.github.com/en/rest/teams/discussions#create-a-discussion
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param discussion_title: string; The discussion post's title.
        :param create_if_not_exists: bool; If discussion does not exists, create one.
        :param private: boolean; Private posts are only visible to team members, organization owners, and team maintainers. Public posts are visible to all members of the organization. Set to true to create a private post.
        :return: request
        '''
        def _search_discussion(discussions: list, search_title: str):
            for discussion in discussions:
                if discussion['title'] == search_title:
                    return discussion

        index = 1

        discussions = self.team_discussion_list(organization_name, team_slug_name, page=index)
        if discussions.status_code >= 300:
            raise Exception(discussions.text)
        discussions = json.loads(discussions.text)

        while len(discussions) > 0:
            discussion = _search_discussion(discussions, discussion_title)
            if discussion is not None:
                return discussion

            index += 1
            discussions = json.loads(self.team_discussion_list(organization_name, team_slug_name, page=index).text)

        if create_if_not_exists:
            return json.loads(self.team_discussion_create(organization_name, team_slug_name, discussion_title, private).text)

    def team_discussion_list(self, organization_name=None, team_slug_name=None, per_page=30, page=1):
        '''
        This method list all discussions on a team's page.
        According API docs: https://docs.github.com/en/rest/teams/discussions#list-discussions
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        body = {}
        query = "?per_page=" + str(per_page) + "&page=" + str(page)
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions" + query
        return self.__request("GET", url.lower(), body)

    def team_discussion_create_comment(self, organization_name=None, team_slug_name=None, discussion_number=None, comment_body=None):
        '''
        This method creates a new comment on a team discussion.
        According API docs: https://docs.github.com/en/rest/teams/discussion-comments#create-a-discussion-comment
        :param organization_name: string; name of the current organization created at github
        :param team_slug_name: string; Github Team slug name
        :param discussion_number: string; The number that identifies the discussion.
        :param comment_body: string; The discussion comment's body text.
        :return: request
        '''
        body = {
            'body': comment_body
        }
        url = self.github_url + "/orgs/" + organization_name + "/teams/" + team_slug_name + "/discussions/" + str(discussion_number) + "/comments"
        return self.__request("POST", url, body)

    def list_repositories(self, organization_name=None, type="all", sort="created", per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object of repositories in a GitHub organization
        According API docs: https://docs.github.com/es/rest/reference/repos#list-organization-repositories
        :param organization_name: string; name of the current organization created at github
        :param type: string; Specifies the types of repositories you want returned. Can be one of all, public, private, forks, sources, member, internal. Default: all
        :param sort: string; Can be one of created, updated, pushed, full_name. Default: created
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)+"&type="+type+"&sort="+sort
        url = self.github_url + "/orgs/" + organization_name + "/repos"+query
        return self.__request("GET", url, params)
        
    def list_repositories_all(self, organization_name=None, type="all", sort="created", per_page = 30):
        '''
        This method allows listing all repositories in a GitHub organization, without paginate option using the method self.list_repositories
        According API docs: https://docs.github.com/es/rest/reference/repos#list-organization-repositories
        :param organization_name: string; name of the current organization created at github
        :param type: string; Specifies the types of repositories you want returned. Can be one of all, public, private, forks, sources, member, internal. Default: all
        :param sort: string; Can be one of created, updated, pushed, full_name. Default: created
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of repositories
        '''
        page = 1
        result = self.__response_to_json(self.list_repositories(organization_name, type="all", sort="created", per_page=per_page, page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self.__response_to_json(self.list_repositories(organization_name, type="all", sort="created", per_page=per_page, page=page))
        return result_all
    
    def repository(self, owner=None, repository_name=None):
        '''
        This method allows getting all repository's details
        According API docs: https://docs.github.com/es/rest/reference/repos#get-a-repository
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :return: request
        '''
        params = {}
        url = self.github_url + "/repos/" + owner + "/" + repository_name
        return self.__request("GET", url, params)
    
    def repository_branch_delete(self, owner=None, repository_name=None, branch_name=None):
        '''
        This method allows remove a repository branch
        According non documented API endpoint mentioned in https://github.community/t/how-to-delete-a-branch-through-the-api/211792
        curl -s -X DELETE -u username:${{secrets.GITHUB_TOKEN}} https://api.github.com/repos/${{ github.repository }}/git/refs/heads/${{ github.head_ref }}
        requests.delete(f"{API_URL}/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH_NAME}")
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param branch_name: string; branch name to be deleted from the repository
        :return: request
        '''
        url = f"{self.github_url}/repos/{owner}/{repository_name}/git/refs/heads/{branch_name}"
        params = {}
        return self.__request("DELETE", url, params)

    def list_repository_branches(self, owner=None, repository_name=None, protected=None, per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object of branches in a repository
        According API docs: https://docs.github.com/es/rest/reference/branches#list-branches
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :protected: string; Setting to true returns only protected branches. When set to false, only unprotected branches are returned. Omitting this parameter returns all branches.
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        if protected:
            params['protected'] = protected
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/branches" + query
        return self.__request("GET", url, params)

    def list_repository_branches_all(self, owner=None, repository_name=None, protected=None, per_page=30):
        '''
        This method allows listing all branches in a repository, without paginate option using the method self.list_repository_branches.
        According API docs: https://docs.github.com/es/rest/reference/branches#list-branches
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :protected: string; Setting to true returns only protected branches. When set to false, only unprotected branches are returned. Omitting this parameter returns all branches.
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of branches
        '''
        page = 1
        result = self.__response_to_json(self.list_repository_branches(owner=owner, repository_name=repository_name, protected=None, per_page=per_page, page=1))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self.__response_to_json(self.list_repository_branches(owner=owner, repository_name=repository_name, protected=None, per_page=per_page, page=page))
        return result_all
    
    def recursive_get_all_repository_branches(self, organization_name, repository_name, page=1):
        '''
        This is a recursive method to get all repository branches using the method self.list_repository_branches
        :param organization_name: string; name of the current organization created at github
        :param repository_name: string; repository slug name
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: Array of branches
        '''
        page_size = 30
        list_branches = json.loads(self.list_repository_branches(owner=organization_name,repository_name=repository_name,per_page=page_size,page=page).text)
        if len(list_branches) == page_size:
            list_branches = list_branches + self.recursive_get_all_repository_branches(organization_name,repository_name,page+1)
        else:
            return list_branches
        return list_branches

    def repository_get_commit_details(self, owner, repository_name, reference, per_page=30, page=1):
        '''
        This method allows listing all details in a commit
        According API docs: https://docs.github.com/es/rest/reference/commits#get-a-commit
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param reference: string; ref parameter
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: commit details
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/commits/" + reference + query
        return self.__request("GET", url, params)

    def repository_comment_issue(self, owner, repository_name, pull_number, body_text):
        '''
        This method allows create a comment in a pull request issue
        According API docs: https://docs.github.com/en/rest/reference/pulls#create-a-review-comment-for-a-pull-request
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param pull_number: int; pull request id number
        :param body_text: string; text of the review comment
        :return: requests details
        '''
        params = {}
        if body_text:
            params['body'] = body_text
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/issues/" + str(pull_number) + "/comments"
        print(url)
        print(body_text)
        return self.__request("POST", url, params)

    def user_details(self, user_name=None):
        '''
        This method allows list all GitHub user properties
        According API docs: https://docs.github.com/es/rest/users/users#get-a-user
        :param organization_name: string; name of the current organization created at github
        :param user_name: string; Github User Name
        :return: request
        '''
        params = {}
        url = self.github_url + "/users/" + user_name
        return self.__request("GET", url, params)

    def repository_create_release(self, owner=None, repository_name=None, tag_name=None, release_name=None, release_body=None, generate_release_notes=False):
        '''
        This method creates a new comment on a team discussion.
        According API docs: https://docs.github.com/en/rest/releases/releases#create-a-release
        :param owner: string; The account owner of the repository. The name is not case sensitive.
        :param repository_name: string; The name of the repository. The name is not case sensitive.
        :param tag_name: string; The name of the tag.
        :param release_name: string; The name of the release.
        :param release_body: string; Text describing the contents of the tag.
        :param generate_release_notes: bool; Whether to automatically generate the name and body for this release. If name is specified, the specified name will be used; otherwise, a name will be automatically generated. If body is specified, the body will be pre-pended to the automatically generated notes.
        :return: request
        '''
        body = {
            'tag_name': tag_name,
            'name': release_name,
            'body': release_body,
            'generate_release_notes': generate_release_notes
        }
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/releases"
        return self.__request("POST", url, body)

    def list_repository_teams(self, owner=None, repository_name=None, per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object branches in a repository
        According API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/teams" + query
        return self.__request("GET", url, params)

    def list_repository_teams_all(self, owner=None, repository_name=None,per_page=30):
        '''
        This method allows listing all branches in a repository, without paginate option using the method self.list_repository_teams.
        According API docs: https://docs.github.com/es/rest/repos/repos#list-repository-teams
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Teams
        '''
        page = 1
        result = self.__response_to_json(self.list_repository_teams(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self.__response_to_json(self.list_repository_teams(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        return result_all
    
    def team_by_name(self, owner=None, team_slug=None):
        '''
        This method allows gets a team using the team's slug
        According API docs:  https://docs.github.com/es/rest/teams/teams#get-a-team-by-name
        :param owner: string; name of the current organization created at github or the owner
        :param team_slug: string; team slug name
        :return: request
        '''
        params = {}
        url = self.github_url + "/orgs/" + owner + "/teams/" + team_slug 
        return self.__request("GET", url, params)
    

    def list_repository_tags(self, owner=None, repository_name=None, per_page=30, page=1):
        '''
        This method allows retreive paginated list in a request object of tags in a repository
        According API docs: https://docs.github.com/en/rest/repos/repos#list-repository-tags
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :return: request
        '''
        params = {}
        query = "?per_page="+str(per_page)+"&page="+str(page)
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/tags" + query
        return self.__request("GET", url, params)
    
    def list_repository_tags_all(self, owner=None, repository_name=None,per_page=30):
        '''
        This method allows listing all tags in a repository, without paginate option using the method self.list_repository_tags.
        According API docs: https://docs.github.com/en/rest/repos/repos#list-repository-tags
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :return: Array of Tags
        '''
        page=1
        result = self.__response_to_json(self.list_repository_tags(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self.__response_to_json(self.list_repository_tags(owner=owner, repository_name=repository_name, per_page=per_page, page=page))
        return result_all
    
    def list_repository_prs(self, owner=None, repository_name=None, per_page=30, page=1, state="all"):
        '''
        This method allows retreive paginated list in a request object of pull request in a repository by status
        According API docs: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param page: integer; Page number of the results to fetch. Default: 1
        :param state: string options separated by comma; options: open, closed, or all
        :return: request
        '''
        params = {}
        query = f"?per_page={str(per_page)}&page={str(page)}&state={state}"
        url = self.github_url + "/repos/" + owner + "/" + repository_name + "/pulls" + query
        return self.__request("GET", url, params)

    def list_repository_prs_all(self, owner=None, repository_name=None,per_page=30,state="all"):
        '''
        This method allows listing all pull request in a repository by status without paginate option using the method self.list_repository_prs.
        According API docs: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :param per_page: integer; Results per page (max 100). Default: 30
        :param state: string options separated by comma; options: open, closed, or all
        :return: Array of Pull Request
        '''
        page=1
        result = self.__response_to_json(self.list_repository_prs(owner=owner, repository_name=repository_name, per_page=per_page, page=page,state=state))
        result_all = []
        while (len(result)>0):
            page +=1
            result_all.extend(result)
            result = self.__response_to_json(self.list_repository_prs(owner=owner, repository_name=repository_name, per_page=per_page, page=page,state=state))
        return result_all
    
    #GraphQL Endpoints

    def delete_repository_branch_protection_rule(self,repository_rule):
        '''
        This method allows delete specific branch protection rule in a repository
        According API docs: https://docs.github.com/es/graphql/reference/mutations#deletebranchprotectionrule
        :param repository_rule: object deleteBranchProtectionRuleInput; https://docs.github.com/es/graphql/reference/input-objects#deletebranchprotectionruleinput
        :return: request
        '''
        query = 'mutation{\
                    deleteBranchProtectionRule(input: { \
                                branchProtectionRuleId: "change_branchProtectionRuleId" \
                    })\
                    {\
                        clientMutationId \
                    }\
            }'
        
        query = query.replace("change_branchProtectionRuleId",str(repository_rule['id'] ))
        query = query.replace("\'","\"")
        myjson = { 'query' : query}
        headers = {'Authorization': 'token %s' % self.__token,
                #'Content-Type': 'application/json'
                }
        response = requests.post(url=self.github_url_graphql, json=myjson, headers=headers,proxies=self.proxies)
        #if(response.status_code >= 200 and response.status_code <= 205):
        #    print(f"For repository: {repository_name} in Github | Delete rule with pattern \"{repository_rule['pattern']}\"")
        return response
    
    def list_repository_branch_protection_rules(self, owner=None, repository_name=None):
        '''
        This method allows list all branch protection rules in a specific repository
        According Github docs: https://github.com/orgs/community/discussions/24596
        :param owner: string; name of the current organization created at github or the owner
        :param repository_name: string; repository slug name
        :return: Array of branch rules
        '''
        list_result = []
        query = '{ repository ( owner:"org_name" , name: "repo_name" )\
            { \
                branchProtectionRules(first: 100) { \
                    nodes { \
                        id \
                        pattern \
                        isAdminEnforced \
                        allowsDeletions \
                        allowsForcePushes \
                        blocksCreations  \
                        bypassForcePushAllowances (first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                        bypassPullRequestAllowances (first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                        pushAllowances(first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                    ... on App { name id } \
                                } \
                            } \
                        } \
                        requiredApprovingReviewCount \
                        requiredStatusCheckContexts \
                        requiredStatusChecks{context} \
                        requiresApprovingReviews \
                        requiresCodeOwnerReviews \
                        requiresCommitSignatures \
                        requiresConversationResolution \
                        requiresStatusChecks \
                        requiresStrictStatusChecks \
                        restrictsPushes \
                        requiresLinearHistory \
                        restrictsReviewDismissals \
                        reviewDismissalAllowances(first: 100) { \
                            totalCount \
                            nodes{  \
                                actor { \
                                    ... on Team { name id } \
                                    ... on User { login id } \
                                } \
                            } \
                        } \
                    } \
                } \
            } \
        } '
        
        query = query.replace("org_name",owner)
        query = query.replace("repo_name",repository_name)
        
        myjson = { 'query' : query}
        headers = {'Authorization': 'token %s' % self.__token}
        response = requests.post(url=self.github_url_graphql, json=myjson, headers=headers,proxies=self.proxies)
        
        if(response.status_code >= 200 and response.status_code <= 205):
            result = json.loads(response.content)
            list_result = result['data']['repository']['branchProtectionRules']['nodes']
        else:
            print(f"There was an error in request: {str(response.content)}")

        return list_result
    
    def create_repository_branch_protection_rule_by_template(self,rule_template,repo_github):
        '''
        This method allows create a branch protection rule defined in a repository template to a specific repository
        According Github docs: https://docs.github.com/es/graphql/reference/mutations#createbranchprotectionrule
        :param rule_template: Object Branch Protection Rule. Params in https://docs.github.com/es/graphql/reference/objects#branchprotectionrule
                              Use method self.list_repository_branch_protection_rules to get specific branch permission rule as a rule template
        :param repo_github: Object Repository; use self.repository to get content body Object (dictionary from JSON)
        :return: Array of branch rule created
        '''
        list_result = [] 
        query = ""
        query = 'mutation{\
                    createBranchProtectionRule(input: { \
                                repositoryId: "change_repositoryId" \
                                pattern: "change_pattern" \
                                allowsDeletions:  change_allowsDeletions\
                                allowsForcePushes: change_allowsForcePushes\
                                blocksCreations: change_blocksCreations\
                                bypassForcePushActorIds: change_bypassForcePushActorIds\
                                bypassPullRequestActorIds: change_bypassPullRequestActorIds\
                                isAdminEnforced: change_isAdminEnforced\
                                pushActorIds: change_pushActorIds\
                                requiredApprovingReviewCount: change_requiredApprovingReviewCount\
                                requiredStatusCheckContexts: change_requiredStatusCheckContexts\
                                requiresApprovingReviews: change_requiresApprovingReviews\
                                requiresCodeOwnerReviews: change_requiresCodeOwnerReviews\
                                requiresCommitSignatures: change_requiresCommitSignatures\
                                requiresConversationResolution: change_requiresConversationResolution\
                                requiresLinearHistory: change_requiresLinearHistory\
                                requiresStatusChecks: change_requiresStatusChecks\
                                requiresStrictStatusChecks: change_requiresStrictStatusChecks\
                                restrictsPushes: change_restrictsPushes\
                                restrictsReviewDismissals: change_restrictsReviewDismissals\
                                reviewDismissalActorIds: change_reviewDismissalActorIds\
                    })\
                    {\
                        clientMutationId\
                        branchProtectionRule{pattern}\
                    }\
            }'
    
        repositoryId = repo_github['node_id'] 
        query = query.replace("change_repositoryId",str(repositoryId))
        
        pattern = rule_template["pattern"] #String
        query = query.replace("change_pattern",pattern)
        
        allowsDeletions = rule_template["allowsDeletions"] #Boolean
        query = query.replace("change_allowsDeletions",str(allowsDeletions).lower())
        
        allowsForcePushes = rule_template["allowsForcePushes"] #Boolean
        query = query.replace("change_allowsForcePushes",str(allowsForcePushes).lower())
        
        blocksCreations = rule_template["blocksCreations"] #Boolean
        query = query.replace("change_blocksCreations",str(blocksCreations).lower())
        
        bypassForcePushActorIds = self.__get_ids_bprotecion(rule_template["bypassForcePushAllowances"],rule_template["bypassForcePushAllowances"]) #IDs list
        query = query.replace("change_bypassForcePushActorIds",str(bypassForcePushActorIds))

        bypassPullRequestActorIds = self.__get_ids_bprotecion(rule_template["bypassPullRequestAllowances"],rule_template["bypassPullRequestAllowances"]) #IDs list
        query = query.replace("change_bypassPullRequestActorIds",str(bypassPullRequestActorIds))
        
        isAdminEnforced = rule_template["isAdminEnforced"] #Boolean
        query = query.replace("change_isAdminEnforced",str(isAdminEnforced).lower())
        
        pushActorIds = self.__get_ids_bprotecion(rule_template["pushAllowances"],rule_template["pushAllowances"]) #IDs list
        query = query.replace("change_pushActorIds",str(pushActorIds))
        
        requiredApprovingReviewCount = rule_template["requiredApprovingReviewCount"] #Boolean
        query = query.replace("change_requiredApprovingReviewCount",str(requiredApprovingReviewCount).lower()) #int
        
        requiresStatusChecks = rule_template["requiresStatusChecks"] #Boolean
        query = query.replace("change_requiresStatusChecks",str(requiresStatusChecks).lower()) #int
        
        requiredStatusCheckContexts = rule_template["requiredStatusCheckContexts"] #[String!]
        query = query.replace("change_requiredStatusCheckContexts",str(requiredStatusCheckContexts))
        
        requiresApprovingReviews = rule_template["requiresApprovingReviews"] #Boolean
        query = query.replace("change_requiresApprovingReviews",str(requiresApprovingReviews).lower())
        
        requiresCodeOwnerReviews = rule_template["requiresCodeOwnerReviews"] #Boolean
        query = query.replace("change_requiresCodeOwnerReviews",str(requiresCodeOwnerReviews).lower())

        requiresCommitSignatures = rule_template["requiresCommitSignatures"] #Boolean
        query = query.replace("change_requiresCommitSignatures",str(requiresCommitSignatures).lower())
        
        requiresConversationResolution = rule_template["requiresConversationResolution"] #Boolean
        query = query.replace("change_requiresConversationResolution",str(requiresConversationResolution).lower())
        
        requiresLinearHistory = rule_template["requiresLinearHistory"] #Boolean
        query = query.replace("change_requiresLinearHistory",str(requiresLinearHistory).lower())
        
        requiresStrictStatusChecks = rule_template["requiresStrictStatusChecks"] #Boolean
        query = query.replace("change_requiresStrictStatusChecks",str(requiresStrictStatusChecks).lower())
        
        restrictsPushes = rule_template["restrictsPushes"] #Boolean
        query = query.replace("change_restrictsPushes",str(restrictsPushes).lower())

        restrictsReviewDismissalsPushes = rule_template["restrictsReviewDismissals"] #Boolean
        query = query.replace("change_restrictsReviewDismissals",str(restrictsReviewDismissalsPushes).lower())
        
        reviewDismissalActorIds = self.__get_ids_bprotecion(rule_template["reviewDismissalAllowances"],rule_template["reviewDismissalAllowances"]) #IDs list
        query = query.replace("change_reviewDismissalActorIds",str(reviewDismissalActorIds))
        query = query.replace("\'","\"")
       
        myjson = { 'query' : query}
        headers = {'Authorization': 'token %s' % self.__token,
                }
        response = requests.post(url=self.github_url_graphql, json=myjson, headers=headers,proxies=self.proxies)
        
        if(response.status_code >= 200 and response.status_code <= 205):
            result = json.loads(response.content)
            print(f"For repo: {repo_github['name']} in Github | Created branch protection rule with pattern \"{result['data']['createBranchProtectionRule']['branchProtectionRule']['pattern']}\"")
        else:
            print(f"There was an error in request: {str(response.content)}")
        
        return list_result

    def __get_ids_bprotecion(self,input_tmp,input_repo):
        result = []
        if input_tmp['totalCount']>0:
            for node in input_tmp['nodes']:
                result.append(node['actor']['id'])
        if input_repo['totalCount']>0:
            for node in input_repo['nodes']:
                if node['actor']['id'] not in result:
                    result.append(node['actor']['id'])
        return result
    