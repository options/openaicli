# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to **[security@yourproject.com]**. You will receive a response from us within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity but historically within a few days.

### What to include in your report

- A description of the vulnerability
- Steps to reproduce the issue
- Possible impact of the vulnerability
- Any suggested mitigation or remediation steps

### What to expect

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide an estimated timeline for addressing the vulnerability
- We will notify you when the vulnerability is fixed
- We may ask for additional information or guidance during the resolution process

### Responsible Disclosure

We ask that you:

- Give us reasonable time to address the issue before making any information public
- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our service
- Only interact with accounts you own or with explicit permission of the account holder

### Recognition

We appreciate your help in keeping OpenAI CLI Tool secure. If you responsibly disclose a security vulnerability, we will:

- Acknowledge your contribution in the project's changelog (unless you prefer to remain anonymous)
- Work with you to understand and resolve the issue quickly

## Security Best Practices

When using this tool:

1. **API Keys**: Never commit API keys to version control. Use environment variables.
2. **File Uploads**: Be cautious when uploading sensitive files to OpenAI services.
3. **Output**: Be aware that generated content may be logged by OpenAI for their service improvement.
4. **Network**: Use secure networks when transmitting data.

## Known Security Considerations

- This tool transmits data to OpenAI's API endpoints
- Uploaded files are processed by OpenAI's services
- Chat conversations may be logged by OpenAI according to their data usage policy
- API keys provide access to your OpenAI account and should be protected

For more information about OpenAI's security practices, please refer to their [security documentation](https://platform.openai.com/docs/guides/safety-best-practices).
