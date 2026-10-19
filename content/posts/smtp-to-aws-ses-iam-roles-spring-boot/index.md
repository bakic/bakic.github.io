---
title: "Migrating from SMTP to AWS SES with IAM Roles: A Security-First Approach to Email in Spring Boot"
date: 2026-01-28
description: "Sending emails is a fundamental requirement for most applications. Whether it’s transactional notifications, alerts, or user communications, we need a..."
categories: [AWS]
tags: [aws, ses, spring-boot, security]
draft: false
---

Sending emails is a fundamental requirement for most applications. Whether it’s transactional notifications, alerts, or user communications, we need a reliable and secure way to dispatch messages.

In this article, I’ll walk through our migration from traditional SMTP authentication to AWS SES with IAM role-based authentication, explaining why this shift represents a significant security improvement.

![Photo by CHUTTERSNAP on Unsplash](image-1.jpg)

*Photo by [CHUTTERSNAP](https://unsplash.com/@chuttersnap?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

## The Traditional Approach: SMTP with Credentials

For years, the standard way to send emails from a Spring Boot application has been through SMTP with username and password authentication:

```yaml
spring:
  mail:
    host: ${SMTP_HOST}
    username: ${SMTP_USERNAME}
    password: ${SMTP_PASSWORD}
    properties:
      mail.transport.protocol: smtp
      mail.smtp.port: ${SMTP_PORT}
      mail.smtp.auth: true
      mail.smtp.starttls.enable: true
      mail.smtp.starttls.required: true
```

The implementation typically uses Spring’s `JavaMailSender`:

```java
@Component
public class EmailPublisher {

    private final JavaMailSender javaMailSender;

    public void sendEmail(String to, String subject, String body) {
        MimeMessage message = javaMailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(body, true);
        javaMailSender.send(message);
    }
}
```

### Why SMTP Has Been the Go-To Choice

SMTP has dominated email delivery for decades, and for good reason. As a standardized protocol defined in RFC 5321, it enjoys universal support across email providers, hosting platforms, and programming languages. This universality means your application can send emails through Gmail today, switch to SendGrid tomorrow, and migrate to a self-hosted mail server next year — all without changing your application code. You simply update the configuration.

This provider-agnostic nature extends to the development experience. Tools like MailHog and Mailcatcher can spin up local SMTP servers in seconds, allowing developers to test email functionality without touching production systems or burning through email quotas. The configuration is straightforward: a host, port, username, and password.

### The Hidden Costs of Simplicity

However, this simplicity comes with significant security trade-offs that are easy to overlook until something goes wrong.

The most obvious concern is credential management. Those SMTP credentials need to live somewhere — environment variables, configuration files, secrets managers — and every location represents a potential leak vector. A misconfigured logging statement might dump environment variables. A developer might accidentally commit credentials to version control. An error page might expose configuration details. These aren’t theoretical risks; they’re incidents that security teams deal with regularly.

Beyond the risk of exposure, there’s the operational burden of credential rotation. When was the last time you rotated your SMTP password? For many teams, the answer is “never” or “only when forced to.” Rotating credentials means updating configuration across all environments, redeploying applications, and hoping nothing breaks. This friction leads to long-lived credentials — exactly what attackers hope to find.

There’s also the problem of credential scope. SMTP credentials typically grant full sending capabilities for an account. If your notification service’s credentials leak, an attacker can send emails as your organization, potentially for phishing campaigns or spam that damages your domain reputation. You can’t easily restrict SMTP credentials to “only send from this address” or “only send to verified recipients.”

Finally, auditing becomes challenging. When something goes wrong — unexpected emails, abuse complaints, quota exhaustion — tracing the source means correlating application logs with email provider logs. If multiple services share credentials, determining which service caused the problem becomes a forensic exercise.

## The New Approach: AWS SES with IAM Roles

AWS Simple Email Service (SES) with IAM role-based authentication eliminates the need for long-lived credentials entirely. Instead, the application assumes an IAM role attached to the infrastructure (EC2, ECS, Lambda, …) and receives temporary credentials automatically.

```java
@Configuration
public class SesConfig {

    @Bean
    public SesClient sesClient() {
        return SesClient.create();
    }
}
```

The `SesClient.create()` method automatically:

- Detects the AWS region from instance metadata  
- Obtains temporary credentials from the IAM role  
- Handles credential refresh transparently

The email publisher becomes:

```java
@Component
public class EmailPublisher {

    private final SesClient sesClient;

    public void sendEmail(String to, String subject, String htmlBody) {
        // Build MIME message for attachments support
        Session session = Session.getDefaultInstance(new Properties());
        MimeMessage message = new MimeMessage(session);
        MimeMessageHelper helper = new MimeMessageHelper(message, true);
        helper.setFrom(fromAddress);
        helper.setTo(to);
        helper.setSubject(subject);
        helper.setText(htmlBody, true);

        // Send via SES
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        message.writeTo(outputStream);

        SendRawEmailRequest request = SendRawEmailRequest.builder()
                .rawMessage(RawMessage.builder()
                        .data(SdkBytes.fromByteArray(outputStream.toByteArray()))
                        .build())
                .build();

        sesClient.sendRawEmail(request);
    }
}
```

### IAM Policy Required

The EC2/ECS instance role needs minimal permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
```

For even tighter security, you can restrict to specific verified identities:

```json
{
    "Resource": "arn:aws:ses:eu-west-1:123456789:identity/yourdomain.com"
}
```

### The Security Model That Eliminates Credentials

The fundamental shift with IAM roles is moving from “something you know” (credentials) to “something you are” (infrastructure identity). Your application doesn’t authenticate with a password; it authenticates by virtue of running on authorized infrastructure. This distinction has profound security implications.

When your application runs on an EC2 instance or ECS task with an attached IAM role, the AWS SDK automatically contacts the instance metadata service to obtain temporary credentials. These credentials typically expire within hours and are automatically refreshed — no application code required. If an attacker somehow extracts these credentials, they have a limited window to exploit them, and the credentials only work for the specific actions permitted by the IAM policy.

This model enables true least-privilege access. Instead of all-or-nothing SMTP credentials, IAM policies let you specify exactly what each service can do. Your notification service might only send emails from `[noreply@yourdomain.com](mailto:noreply@yourdomain.com)`, while your marketing platform can send from `[marketing@yourdomain.com](mailto:marketing@yourdomain.com)`. If one service is compromised, the blast radius is contained.

The audit story transforms completely. Every SES API call is logged in CloudTrail with the IAM role identity, timestamp, source IP, and request parameters. When investigating an incident, you can immediately identify which service, on which infrastructure, sent which emails. This traceability is invaluable for compliance requirements and incident response.

Perhaps most importantly, there are simply no credentials to leak. No passwords in environment variables, no secrets to accidentally commit, no configuration files to protect. You can’t leak what doesn’t exist.

### The Trade-offs to Consider

This approach isn’t without its challenges, and teams should evaluate whether the benefits outweigh the costs for their specific situation.

The most significant consideration is AWS lock-in. By adopting SES with IAM roles, your email-sending infrastructure becomes tightly coupled to AWS. Migrating to another cloud provider or on-premises infrastructure would require rearchitecting your email delivery. For organizations committed to AWS, this is rarely a concern. For multi-cloud strategies, it might be a dealbreaker.

Local development requires more thought. Developers can’t simply point at a local SMTP server anymore. You’ll need to either mock the SES client in tests, provide developers with AWS credentials for a sandbox account, or maintain a parallel SMTP configuration for local development. None of these options are difficult, but they add complexity compared to the “just run MailHog” experience.

There’s also a learning curve for teams unfamiliar with IAM. Understanding roles, policies, trust relationships, and the credential provider chain takes time. A misconfigured IAM policy might silently deny access, leading to confusing debugging sessions. However, this investment in IAM knowledge pays dividends across all AWS services, not just SES.

Finally, SES has its own requirements. You must verify domain ownership, and new accounts start in sandbox mode where you can only send to verified addresses. Moving to production requires a request to AWS. Your domain needs proper SPF, DKIM, and DMARC configuration. These aren’t disadvantages per se — any reputable email provider requires similar verification — but they represent work that SMTP-based services sometimes let you skip.

## Best Practices

### 1. Use IAM Roles Whenever Possible

If you’re running on AWS infrastructure, always prefer IAM roles over static credentials. This applies to all AWS services, not just SES.

### 2. Apply Least Privilege

Don’t use `”Resource”: “\*”` in production. Restrict to specific verified identities:

```json
{
    "Action": ["ses:SendEmail", "ses:SendRawEmail"],
    "Resource": [
        "arn:aws:ses:eu-west-1:ACCOUNT:identity/notifications@yourdomain.com"
    ]
}
```

### 3. Use Condition Keys for Extra Security

Restrict who can send emails and to whom:

```perl
{
    "Condition": {
        "StringEquals": {
            "ses:FromAddress": "noreply@yourdomain.com"
        }
    }
}
```

### 4. Enable SES Configuration Sets

When you send emails through SES, your messages enter a complex ecosystem where many things can go wrong. The recipient’s mailbox might be full. The email address might not exist. The recipient might mark your email as spam. Without visibility into these events, you’re flying blind — and the consequences can be severe.

### Why Configuration Sets Matter

Amazon SES maintains a reputation score for your sending identity based on bounces, complaints, and engagement metrics. If your bounce rate exceeds 5% or your complaint rate exceeds 0.1%, SES may throttle or suspend your sending capabilities. The problem? By the time you notice emails aren’t being delivered, the damage to your reputation is already done.

Configuration Sets solve this by providing real-time event tracking for every email you send. When you associate a Configuration Set with your emails, SES publishes delivery events to destinations of your choice — SNS topics, CloudWatch, Kinesis Firehose, or EventBridge. This transforms email sending from a fire-and-forget operation into an observable, manageable process.

### What Events Can You Track?

Configuration Sets capture the complete lifecycle of an email:

- **Send**: The email was accepted by SES for delivery  
- **Delivery**: The recipient’s mail server accepted the email  
- **Bounce**: The email couldn’t be delivered (hard bounce = invalid address, soft bounce = temporary issue)  
- **Complaint**: The recipient marked your email as spam  
- **Reject**: SES refused to send the email (virus detected, suppression list)  
- **Open**: The recipient opened the email (requires tracking pixel)  
- **Click**: The recipient clicked a link (requires link rewriting)  
- **Rendering Failure**: Template rendering failed

### Real-World Problems Configuration Sets Solve

**Scenario 1: The Silent Bounce Storm**

Imagine your marketing team uploads a customer list that hasn’t been cleaned in years. Thousands of emails go out, and 15% bounce because the addresses no longer exist. Without a Configuration Set, you might not discover this until SES sends you a warning — or worse, suspends your account. With event tracking, you can set up a CloudWatch alarm that triggers when bounce rates spike, allowing you to pause the campaign before it destroys your sender reputation.

**Scenario 2: The Compliance Nightmare**

A user complains to your support team that they never subscribed to your emails. Did they actually receive the email? Did they click the unsubscribe link? Without delivery tracking, you’re guessing. With Configuration Sets publishing to CloudWatch Logs or S3, you have an auditable record of every email interaction — invaluable for GDPR compliance and dispute resolution.

**Scenario 3: The Invalid Address Database**

Your application sends transactional emails to user-provided addresses. Some users mistype their email, others abandon accounts, and some addresses become invalid over time. Each bounce hurts your reputation. By streaming bounce events to an SNS topic, you can automatically update your database to mark invalid addresses, preventing repeated bounces to the same address.

### 5. Handle Local Development

Create a separate profile for local development that either:

- Mocks the email sender
- Uses a local SMTP server like MailHog
- Uses AWS credentials from `~/.aws/credentials` for developer accounts

```java
@Configuration
@Profile("local")
public class LocalEmailConfig {

    @Bean
    public SesClient sesClient() {
        // Use default credential provider chain for local dev
        return SesClient.builder()
                .region(Region.EU_WEST_1)
                .build();
    }
}
```

### 6. Monitor and Alert

Set up CloudWatch alarms for:

. Bounce rates exceeding thresholds

. Complaint rates

Send quota utilization

## Conclusion

While SMTP with credentials remains a valid option for certain use cases (multi-cloud, on-premises), **AWS SES with IAM roles is the clear winner for applications running on AWS infrastructure**. The security benefits are substantial:

- **Zero credential management** eliminates an entire class of security vulnerabilities  
- **Automatic rotation** removes operational burden  
- **Fine-grained IAM policies** enforce least privilege  
- **CloudTrail integration** provides comprehensive audit trails

The slight increase in AWS coupling is a worthwhile trade-off for most organizations already invested in the AWS ecosystem. The migration is straightforward, and the security posture improvement is immediate and significant.

In an era where credential leaks make headlines regularly, removing credentials entirely isn’t just a best practice — it’s the responsible choice.
