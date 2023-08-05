# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Generated code. DO NOT EDIT!
#
# Snippet for MethodBidiStreaming
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install animalia-mollusca


# [START mollusca_v1_generated_Snippets_MethodBidiStreaming_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from animalia import mollusca_v1


def sample_method_bidi_streaming():
    # Create a client
    client = mollusca_v1.SnippetsClient()

    # Initialize request argument(s)
    request = mollusca_v1.SignatureRequestOneRequiredField(
        my_string="my_string_value",
    )

    # This method expects an iterator which contains
    # 'mollusca_v1.SignatureRequestOneRequiredField' objects
    # Here we create a generator that yields a single `request` for
    # demonstrative purposes.
    requests = [request]

    def request_generator():
        for request in requests:
            yield request

    # Make the request
    stream = client.method_bidi_streaming(requests=request_generator())

    # Handle the response
    for response in stream:
        print(response)

# [END mollusca_v1_generated_Snippets_MethodBidiStreaming_sync]
