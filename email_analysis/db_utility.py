#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility class to create entities in the database."""

import hashlib

from .models import Email, Host, IPAddress, Url


def find_email_id(email_body):
    """Find the hash of the given email_body."""
    return hashlib.md5(email_body.encode('utf-8')).hexdigest()


class DBEntityCreator():
    """Class for creating things in the database."""

    def __init__(self, incoming_post_content):
        """."""
        self.post_content = incoming_post_content
        self.create_email()
        self.create_network_data()

    def create_email(self):
        """Create an email entity."""
        # TODO: When I start storing the emails as files, replace the full_text variable below
        full_email_text = "This is just a placeholder text"
        email_subject = self.post_content.get('email_subject')
        recipient_email = self.post_content.get('recipient_email')
        sender_email = self.post_content.get('sender_email')
        sender_ip = self.post_content.get('sender_ip')
        email_id = find_email_id(full_email_text)

        new_email = Email(full_text=full_email_text, subject=email_subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip, submitter="12345678", id=email_id)
        new_email.save()

        self.email = new_email
        return

    def create_network_data(self):
        """Create all of teh hosts, ips, and urls in the email."""
        for entry in self.post_content:
            if entry.startswith("host-"):
                # create a host
                new_host = Host(host_name=entry[5:], source="b")
                new_host.save()
                new_host.emails.add(self.email)
            elif entry.startswith("ip-"):
                # create an ip address
                new_ip = IPAddress(ip_address=entry[3:])
                new_ip.save()
                new_ip.emails.add(self.email)
            elif entry.startswith("url-"):
                # create a url
                # TODO: parse query strings, url path, and host name out of the URL more robustly (2)
                url = entry[4:]
                url_path = entry[4:].split("/")[1]
                host = entry[4:].split("/")[0]
                print("host: {}".format(host))
                url_host_name = Host(host_name=host, source="b")
                url_host_name.save()
                url_host_name.emails.add(self.email)

                new_url = Url(url=url, host=url_host_name)

                if url_path is not None:
                    new_url.url_path = url_path

                new_url.save()
                new_url.emails.add(self.email)
