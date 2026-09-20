# Lab 11 Model Answers

## Verified Output

Run for real, building on Module 6's ECR repository and Module 7's cluster and execution role:

- `leap-jenkins-deploy-role` created, trust policy scoped to `ec2.amazonaws.com` specifically -
  verified directly with `aws iam get-role`, not assumed from the console.
- `leap-jenkins-deploy-profile` instance profile created and the role added to it - verified with
  `aws iam get-instance-profile`.
- A permissions policy scoped to four statements (`ECRAuth`, `ECRPush`, `ECSDeploy`,
  `PassExecutionRoleOnly`), each naming a specific resource ARN where the action supports it.
- Docker login, build, and push executed directly: a digest returned from ECR, confirming the
  push succeeded.
- A task definition built from the current live one via `describe-task-definition`, image
  swapped, registered as a new revision and run successfully - CloudWatch logs confirmed a
  Spring Boot startup from the newly built image.

## The Reflection Question

A long-lived AWS access key stored as a Jenkins credential keeps working indefinitely, regardless
of who created it, whether they still work on the project, or whether the Jenkins server it was
configured on still exists. Decommissioning the Jenkins server doesn't revoke the key - it's an
IAM identity in AWS, entirely independent of the server. If the person who originally created it
leaves, the key doesn't know that either; it keeps authenticating successfully until someone
remembers it exists and manually finds and revokes it, which is easy to forget, especially months
later, and there's no reliable way to audit "which stored credentials belong to a decommissioned
server or a person who's left" without deliberately tracking it.

An instance profile has no equivalent problem, because there's no long-lived credential to revoke
in the first place. Credentials are vended by AWS to the EC2 instance itself, automatically
rotated, and valid only as long as that specific instance exists and the profile stays attached.
Terminating the Jenkins EC2 instance ends its access immediately and automatically - there's
nothing left over to remember to clean up, and nothing tied to any individual person's continued
employment at all.
