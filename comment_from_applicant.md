# frozen-desserts

## How it was
After reading the README.md I thought to use only mentioned tools such as Github Actions and AWS free tier resourses.
But curiousity towards Pulumi couldn't let me be.
So I decided to give it a good try and spin up building and deployment phases of application lifecycle with Pulumi
I went through the path of dockerizing the app, and manual deploying it, but not all the resourses shoul be deployed automatically
And therefore I splitted the Pulumi stack into two parts - manual (for potential admin to run) and auto (which wiil runs automatically by Github Actions)
After doing that I realized that the testing step is missing
Frankly speaking I tried to comply with the acceptance criteria "it should run the specs and fail to deploy if the specs fail" doing this part with Pulumi
But to my sadness nothing came to mind how to handle this. As my tries to run RSpeck inside the container and catching container logs afterwards were unsuccessful. Due to the pulumi.Output object type which was the main problem here.
So, I moved to a more simple solution of using Github actions instead
The service is fully created and working now
I tried to achive all the criteria and had a lot of fun doing it!
I would love to know even more solutions how to work with Pulumi from you and also to hear any feedback about this small assesment
Thank you!

PS: I purposely didn't multiplicate branches for different environments and didn't try to create deployment template to potential different envs just to save time. Also I didn't create replica for a db as it wasn't needed to achieve fault-tolerance of a database. But I know that it could be done if needed =)
BTW, for local tests I used docker-compose file but avoid to use it inside the Github actions just because it was unnecessary
Usually for the final decisions which tools and how thase used I disscuss my strategy with somebody from the team. It's a necessary step for my opinion bacause the solution shoul be reusable and useful for others too and not just for me

## Acceptance Criteria from the README.md
Acceptance criteria are listed in descending order of importance. Things closer to the bottom should be considered “stretch goals”. For example, you could deploy a version of this that uses sqlite and loses data when it is redeployed until you are able to persist data in a database.

1. it should fork the repo at https://github.com/strongmind/frozen-desserts - check
2. it should deploy automatically from github using github actions every time the main branch is updated - check
3. it should run the specs and fail to deploy if the specs fail - check
4. it should be available from the internet via http or https - check
5. it should recreate AWS resources if they are destroyed
6. it should persist data in a database