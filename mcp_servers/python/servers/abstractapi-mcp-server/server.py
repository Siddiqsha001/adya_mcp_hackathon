import os
from typing import Any

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("abstract_api")


# Constants
ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "your_api_key_here")
ABSTRACT_API_URL = "https://emailvalidation.abstractapi.com/v1/"
PHONE_VALIDATION_API_URL = "https://phonevalidation.abstractapi.com/v1/"
EMAIL_REPUTATION_API_URL = "https://emailreputation.abstractapi.com/v1/"


@mcp.tool()
async def verify_email(email: str) -> dict[str, Any]:
    """
    Validates an email address using an external email validation API of abstractapi.

    This function checks the validity, deliverability, and other attributes of an email address.
    It returns a detailed dictionary containing information about the email's format, domain,
    and SMTP server.

    Args:
        email (str): The email address to validate.

    Returns:
        dict[str, Any]: A dictionary containing detailed validation results. The dictionary
        includes the following keys:
            - "email" (str): The email address being validated.
            - "autocorrect" (str): Suggested autocorrection if the email is invalid or malformed.
            - "deliverability" (str): The deliverability status of the email (e.g., "DELIVERABLE").
            - "quality_score" (str): A score representing the quality of the email address.
            - "is_valid_format" (dict): Whether the email is in a valid format.
                - "value" (bool): True if the format is valid, False otherwise.
                - "text" (str): A textual representation of the format validity (e.g., "TRUE").
            - "is_free_email" (dict): Whether the email is from a free email provider.
                - "value" (bool): True if the email is from a free provider, False otherwise.
                - "text" (str): A textual representation (e.g., "TRUE").
            - "is_disposable_email" (dict): Whether the email is from a disposable email service.
                - "value" (bool): True if the email is disposable, False otherwise.
                - "text" (str): A textual representation (e.g., "FALSE").
            - "is_role_email" (dict): Whether the email is a role-based email (e.g., "admin@domain.com").
                - "value" (bool): True if the email is role-based, False otherwise.
                - "text" (str): A textual representation (e.g., "FALSE").
            - "is_catchall_email" (dict): Whether the domain uses a catch-all email address.
                - "value" (bool): True if the domain is catch-all, False otherwise.
                - "text" (str): A textual representation (e.g., "FALSE").
            - "is_mx_found" (dict): Whether MX records are found for the email domain.
                - "value" (bool): True if MX records are found, False otherwise.
                - "text" (str): A textual representation (e.g., "TRUE").
            - "is_smtp_valid" (dict): Whether the SMTP server for the email domain is valid.
                - "value" (bool): True if the SMTP server is valid, False otherwise.
                - "text" (str): A textual representation (e.g., "TRUE").

    Example:
        >>> await verify_email("thanos@snap.io")
        {
            "email": "thanos@snap.io",
            "autocorrect": "",
            "deliverability": "UNDELIVERABLE",
            "quality_score": "0.00",
            "is_valid_format": {
                "value": true,
                "text": "TRUE"
            },
            "is_free_email": {
                "value": false,
                "text": "FALSE"
            },
            "is_disposable_email": {
                "value": false,
                "text": "FALSE"
            },
            "is_role_email": {
                "value": false,
                "text": "FALSE"
            },
            "is_catchall_email": {
                "value": false,
                "text": "FALSE"
            },
            "is_mx_found": {
                "value": false,
                "text": "FALSE"
            },
            "is_smtp_valid": {
                "value": false,
                "text": "FALSE"
            }
        }
    Raises:
        ValueError: If the API key is not found in the environment variables.
        requests.exceptions.HTTPError: If the API request fails (e.g., 4xx or 5xx error).
        Exception: For any other unexpected errors.
    """
    # Check if the API key is available
    if not ABSTRACT_API_KEY:
        raise ValueError("API key not found in environment variables.")

    # Construct the API URL
    api_url = f"{ABSTRACT_API_URL}?api_key={ABSTRACT_API_KEY}&email={email}"

    try:
        # Make the API request (ignoring SSL verification)
        response = requests.get(api_url, verify=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Parse the JSON response
        result = response.json()

        # Return the validation results
        return result

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 4xx, 5xx)
        raise requests.exceptions.HTTPError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # Handle any other errors
        raise Exception(f"An error occurred: {err}")


@mcp.tool()
async def validate_phone(phone: str, country: str | None = None) -> dict[str, Any]:
    """
    Validates a phone number using Abstract API's Phone Validation service.

    This function checks the validity and other details of phone numbers from over 190 countries.
    It returns detailed information about the phone number including format, country, location,
    type, and carrier information.

    Args:
        phone (str): The phone number to validate and verify.
        country (str, optional): The country's ISO code to indicate the phone number's country.
                                This helps the API append the corresponding country code to its analysis.
                                For example, use "US" for United States numbers.

    Returns:
        dict[str, Any]: A dictionary containing detailed validation results. The dictionary
        includes the following keys:
            - "phone" (str): The phone number submitted for validation.
            - "valid" (bool): True if the phone number is valid, False otherwise.
            - "format" (dict): Object containing international and local formats.
                - "international" (str): International format with country code and "+" prefix.
                - "local" (str): Local/national format without international formatting.
            - "country" (dict): Object containing country details.
                - "code" (str): Two-letter ISO 3166-1 alpha-2 country code.
                - "name" (str): Name of the country where the phone number is registered.
                - "prefix" (str): Country's calling code prefix.
            - "location" (str): Location details (region, state/province, sometimes city).
            - "type" (str): Type of phone number. Possible values: "Landline", "Mobile",
                           "Satellite", "Premium", "Paging", "Special", "Toll_Free", "Unknown".
            - "carrier" (str): The carrier that the number is registered with.

    Example:
        >>> await validate_phone("14152007986")
        {
            "phone": "14152007986",
            "valid": true,
            "format": {
                "international": "+14152007986",
                "local": "(415) 200-7986"
            },
            "country": {
                "code": "US",
                "name": "United States",
                "prefix": "+1"
            },
            "location": "California",
            "type": "mobile",
            "carrier": "T-Mobile USA, Inc."
        }

        >>> await validate_phone("2007986", "US")
        # Will validate with US country context

    Raises:
        ValueError: If the API key is not found in the environment variables.
        requests.exceptions.HTTPError: If the API request fails (e.g., 4xx or 5xx error).
        Exception: For any other unexpected errors.
    """
    # Check if the API key is available
    if not ABSTRACT_API_KEY:
        raise ValueError("API key not found in environment variables.")

    # Construct the API URL
    api_url = f"{PHONE_VALIDATION_API_URL}?api_key={ABSTRACT_API_KEY}&phone={phone}"

    # Add country parameter if provided
    if country:
        api_url += f"&country={country}"

    try:
        # Make the API request (ignoring SSL verification)
        response = requests.get(api_url, verify=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Parse the JSON response
        result = response.json()

        # Return the validation results
        return result

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 4xx, 5xx)
        raise requests.exceptions.HTTPError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # Handle any other errors
        raise Exception(f"An error occurred: {err}")


@mcp.tool()
async def check_email_reputation(email: str) -> dict[str, Any]:
    """
    Analyzes email reputation using Abstract API's Email Reputation service.

    This function provides comprehensive email reputation analysis including deliverability,
    quality scoring, sender information, domain details, risk assessment, and breach history.
    It's designed to help improve delivery rates, clean email lists, and block fraudulent users.

    Args:
        email (str): The email address to analyze for reputation.

    Returns:
        dict[str, Any]: A dictionary containing comprehensive reputation analysis. The dictionary
        includes the following main sections:
            - "email_address" (str): The email address that was analyzed.
            - "email_deliverability" (dict): Deliverability information.
                - "status" (str): "deliverable", "undeliverable", or "unknown".
                - "status_detail" (str): Additional detail (e.g., "valid_email", "invalid_format").
                - "is_format_valid" (bool): True if email follows correct format.
                - "is_smtp_valid" (bool): True if SMTP check was successful.
                - "is_mx_valid" (bool): True if domain has valid MX records.
                - "mx_records" (list): List of MX records for the domain.
            - "email_quality" (dict): Quality assessment information.
                - "score" (float): Confidence score between 0.01 and 0.99.
                - "is_free_email" (bool): True if from free provider (Gmail, Yahoo, etc.).
                - "is_username_suspicious" (bool): True if username appears auto-generated.
                - "is_disposable" (bool): True if from disposable email provider.
                - "is_catchall" (bool): True if domain accepts all emails.
                - "is_subaddress" (bool): True if uses subaddressing (user+label@domain.com).
                - "is_role" (bool): True if role-based address (info@, support@, etc.).
                - "is_dmarc_enforced" (bool): True if strict DMARC policy enforced.
                - "is_spf_strict" (bool): True if domain enforces strict SPF policy.
                - "minimum_age" (int|null): Estimated age of email address in days.
            - "email_sender" (dict): Sender information if available.
                - "first_name" (str|null): First name associated with email.
                - "last_name" (str|null): Last name associated with email.
                - "email_provider_name" (str|null): Email provider name (e.g., "Google").
                - "organization_name" (str|null): Organization linked to email/domain.
                - "organization_type" (str|null): Type of organization (e.g., "company").
            - "email_domain" (dict): Domain information.
                - "domain" (str): Domain part of the email.
                - "domain_age" (int|null): Age of domain in days.
                - "is_live_site" (bool|null): True if domain has active website.
                - "registrar" (str|null): Domain registrar name.
                - "registrar_url" (str|null): Registrar website URL.
                - "date_registered" (str|null): Domain registration date.
                - "date_last_renewed" (str|null): Last renewal date.
                - "date_expires" (str|null): Domain expiration date.
                - "is_risky_tld" (bool|null): True if top-level domain is considered risky.
            - "email_risk" (dict): Risk assessment.
                - "address_risk_status" (str): Risk level for the email address.
                - "domain_risk_status" (str): Risk level for the domain.
            - "email_breaches" (dict): Data breach information.
                - "total_breaches" (int|null): Number of known breaches.
                - "date_first_breached" (str|null): Date of first known breach.
                - "date_last_breached" (str|null): Date of most recent breach.
                - "breached_domains" (list): List of breached domains with dates.

    Example:
        >>> await check_email_reputation("benjamin.richard@abstractapi.com")
        {
            "email_address": "benjamin.richard@abstractapi.com",
            "email_deliverability": {
                "status": "deliverable",
                "status_detail": "valid_email",
                "is_format_valid": true,
                "is_smtp_valid": true,
                "is_mx_valid": true,
                "mx_records": ["gmail-smtp-in.l.google.com", ...]
            },
            "email_quality": {
                "score": 0.8,
                "is_free_email": false,
                "is_username_suspicious": false,
                "is_disposable": false,
                "is_catchall": true,
                "is_subaddress": false,
                "is_role": false,
                "is_dmarc_enforced": true,
                "is_spf_strict": true,
                "minimum_age": 1418
            },
            "email_sender": {
                "first_name": "Benjamin",
                "last_name": "Richard",
                "email_provider_name": "Google",
                "organization_name": "Abstract API",
                "organization_type": "company"
            },
            "email_domain": {
                "domain": "abstractapi.com",
                "domain_age": 1418,
                "is_live_site": true,
                "registrar": "NAMECHEAP INC",
                "registrar_url": "http://www.namecheap.com",
                "date_registered": "2020-05-13",
                "date_last_renewed": "2024-04-13",
                "date_expires": "2025-05-13",
                "is_risky_tld": false
            },
            "email_risk": {
                "address_risk_status": "low",
                "domain_risk_status": "low"
            },
            "email_breaches": {
                "total_breaches": 2,
                "date_first_breached": "2018-07-23T14:30:00Z",
                "date_last_breached": "2019-05-24T14:30:00Z",
                "breached_domains": [
                    {"domain": "apollo.io", "date_breached": "2018-07-23T14:30:00Z"},
                    {"domain": "canva.com", "date_breached": "2019-05-24T14:30:00Z"}
                ]
            }
        }

    Raises:
        ValueError: If the API key is not found in the environment variables.
        requests.exceptions.HTTPError: If the API request fails (e.g., 4xx or 5xx error).
        Exception: For any other unexpected errors.
    """
    # Check if the API key is available
    if not ABSTRACT_API_KEY:
        raise ValueError("API key not found in environment variables.")

    # Construct the API URL
    api_url = f"{EMAIL_REPUTATION_API_URL}?api_key={ABSTRACT_API_KEY}&email={email}"

    try:
        # Make the API request (ignoring SSL verification)
        response = requests.get(api_url, verify=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Parse the JSON response
        result = response.json()

        # Return the reputation analysis results
        return result

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 4xx, 5xx)
        raise requests.exceptions.HTTPError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        # Handle any other errors
        raise Exception(f"An error occurred: {err}")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
