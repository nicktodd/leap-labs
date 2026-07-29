# Lab 11 Model Answers

## Verified Output

Run for real, building on Module 6's ECR repository and Module 7's cluster and execution role:

- `aws iam create-open-id-connect-provider` for `token.actions.githubusercontent.com`: created
  successfully with the `sts.amazonaws.com` audience.
- `leap-github-actions-deploy-role` created, trust policy scoped to
  `repo:<org>/leap-sprint11:ref:refs/heads/main` specifically — verified directly with
  `aws iam get-role`, not assumed from the console.
- A permissions policy scoped to four statements (`ECRAuth`, `ECRPush`, `ECSDeploy`,
  `PassExecutionRoleOnly`), each naming a specific resource ARN where the action supports it.
- Docker login, build, and push executed directly: a real digest returned from ECR, confirming
  the push succeeded.
- The first deploy attempt, cloning Module 9's task definition revision 3 and swapping only the
  image, failed with a genuine `AccessDeniedException` — revision 3 referenced a Secrets Manager
  secret that Module 9's own cleanup had already deleted, along with the execution role's
  permission to read it.
- A clean task definition, built from the base template rather than an old revision, registered
  as revision 5 and run successfully — real CloudWatch logs confirmed a genuine Spring Boot
  startup from the newly built image.

## The Reflection Question

An AWS access key stored as a GitHub secret keeps working indefinitely, regardless of who created
it or whether they still have any relationship to the project — it has no built-in expiry and no
connection to the identity of a specific team member. If the person who originally created that
key leaves, the key itself doesn't know that; it keeps authenticating successfully until someone
remembers it exists and manually finds and revokes it — a step that's easy to forget, especially
months or years later, and there's no reliable way to audit "which stored secrets belong to
people who've since left" without deliberately tracking it.

The OIDC approach has no equivalent problem, because there's no long-lived credential to revoke
in the first place. Each workflow run gets its own short-lived token from GitHub, valid only for
that run, exchanged for temporary AWS credentials that expire on their own shortly after. Nothing
is tied to an individual person's identity or continued employment — the trust relationship is
between GitHub's token issuer and AWS, scoped to a specific repository and branch, not to a
person who might leave. Removing someone's GitHub access revokes their ability to trigger a new
workflow run; it doesn't require anyone to remember a separate AWS credential exists at all.
