# PaySprint Mobile — Password Reset Flow (Design Document Excerpt)

**Feature: "Forgot Password"**

1. Customer enters their email address and answers one security question (mother's maiden
   name), chosen by the customer when they first registered.
2. If the answer matches, the system looks up the customer's current password and emails it to
   them in plain text, so they can log in again with the password they already know.
3. No limit on how many times a customer (or anyone else) can attempt the security question for
   a given email address.
4. The security question and answer are the same for the lifetime of the account, and cannot be
   changed by the customer.

This is the agreed design for the feature, ready for a developer to implement.
