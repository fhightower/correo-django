#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility class to create entities in the database."""

import hashlib

from django.core.exceptions import ObjectDoesNotExist
import sqlite3

from .models import Email, Host, IPAddress, Url


def create_email_id(email_content):
    """Find the hash of the given email_content."""
    return hashlib.md5(email_content.encode('utf-8')).hexdigest()


class DBEntityCreator():
    """Class for creating things in the database."""

    def __init__(self, incoming_post_content):
        """."""
        self.post_content = incoming_post_content
        self.email_exists = False
        # check to see if the email exists
        if incoming_post_content.get('full_text'):
            full_email_text = incoming_post_content.get('full_text')
        else:
            # TODO: When I start storing the emails as files, replace the full_text variable below
            full_email_text = "This is just a placeholder text"
        email_id = create_email_id(full_email_text)
        self._check_email_exists(email_id)

        # if the email does not exist, create one
        if not self.email_exists:
            # create the email
            self.create_email(email_id, full_email_text)
            # create the network data associated with the email
            self.create_network_data()
        # if the email already exists:
        else:
            # create a simple dict with the id of the email so that the user can be directed to the correct page
            self.email = {
                'id': email_id
            }

    def _check_email_exists(self, email_id):
        """Check to see if an email with the given id already exists in the system."""
        email = None
        try:
            email = Email.objects.get(id=email_id)
        # this error is thrown if the email does not exist in the system
        except ObjectDoesNotExist as e:
            pass

        self.email_exists = email is not None

    def create_email(self, email_id, full_email_text):
        """Create an email entity."""
        # pull all of the important fields from the posted content
        email_subject = self.post_content.get('email_subject')
        recipient_email = self.post_content.get('recipient_email')
        sender_email = self.post_content.get('sender_email')
        sender_ip = self.post_content.get('sender_ip')

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
