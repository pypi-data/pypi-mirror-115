# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1", manifest={"ResponseMessage",},
)


class ResponseMessage(proto.Message):
    r"""Represents a response message that can be returned by a
    conversational agent.

    Response messages are also used for output audio synthesis. The
    approach is as follows:

    -  If at least one OutputAudioText response is present, then all
       OutputAudioText responses are linearly concatenated, and the
       result is used for output audio synthesis.
    -  If the OutputAudioText responses are a mixture of text and SSML,
       then the concatenated result is treated as SSML; otherwise, the
       result is treated as either text or SSML as appropriate. The
       agent designer should ideally use either text or SSML
       consistently throughout the bot design.
    -  Otherwise, all Text responses are linearly concatenated, and the
       result is used for output audio synthesis.

    This approach allows for more sophisticated user experience
    scenarios, where the text displayed to the user may differ from what
    is heard.

    Attributes:
        text (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.Text):
            Returns a text response.
        payload (google.protobuf.struct_pb2.Struct):
            Returns a response containing a custom,
            platform-specific payload.
        conversation_success (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.ConversationSuccess):
            Indicates that the conversation succeeded.
        output_audio_text (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.OutputAudioText):
            A text or ssml response that is
            preferentially used for TTS output audio
            synthesis, as described in the comment on the
            ResponseMessage message.
        live_agent_handoff (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.LiveAgentHandoff):
            Hands off conversation to a human agent.
        end_interaction (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.EndInteraction):
            Output only. A signal that indicates the interaction with
            the Dialogflow agent has ended. This message is generated by
            Dialogflow only when the conversation reaches
            ``END_SESSION`` page. It is not supposed to be defined by
            the user.

            It's guaranteed that there is at most one such message in
            each response.
        play_audio (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.PlayAudio):
            Signal that the client should play an audio clip hosted at a
            client-specific URI. Dialogflow uses this to construct
            [mixed_audio][google.cloud.dialogflow.cx.v3beta1.ResponseMessage.mixed_audio].
            However, Dialogflow itself does not try to read or process
            the URI in any way.
        mixed_audio (google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.MixedAudio):
            Output only. An audio response message composed of both the
            synthesized Dialogflow agent responses and responses defined
            via
            [play_audio][google.cloud.dialogflow.cx.v3beta1.ResponseMessage.play_audio].
            This message is generated by Dialogflow only and not
            supposed to be defined by the user.
    """

    class Text(proto.Message):
        r"""The text response message.
        Attributes:
            text (Sequence[str]):
                Required. A collection of text responses.
            allow_playback_interruption (bool):
                Output only. Whether the playback of this
                message can be interrupted by the end user's
                speech and the client can then starts the next
                Dialogflow request.
        """

        text = proto.RepeatedField(proto.STRING, number=1,)
        allow_playback_interruption = proto.Field(proto.BOOL, number=2,)

    class LiveAgentHandoff(proto.Message):
        r"""Indicates that the conversation should be handed off to a live
        agent.

        Dialogflow only uses this to determine which conversations were
        handed off to a human agent for measurement purposes. What else to
        do with this signal is up to you and your handoff procedures.

        You may set this, for example:

        -  In the
           [entry_fulfillment][google.cloud.dialogflow.cx.v3beta1.Page.entry_fulfillment]
           of a [Page][google.cloud.dialogflow.cx.v3beta1.Page] if entering
           the page indicates something went extremely wrong in the
           conversation.
        -  In a webhook response when you determine that the customer issue
           can only be handled by a human.

        Attributes:
            metadata (google.protobuf.struct_pb2.Struct):
                Custom metadata for your handoff procedure.
                Dialogflow doesn't impose any structure on this.
        """

        metadata = proto.Field(proto.MESSAGE, number=1, message=struct_pb2.Struct,)

    class ConversationSuccess(proto.Message):
        r"""Indicates that the conversation succeeded, i.e., the bot handled the
        issue that the customer talked to it about.

        Dialogflow only uses this to determine which conversations should be
        counted as successful and doesn't process the metadata in this
        message in any way. Note that Dialogflow also considers
        conversations that get to the conversation end page as successful
        even if they don't return
        [ConversationSuccess][google.cloud.dialogflow.cx.v3beta1.ResponseMessage.ConversationSuccess].

        You may set this, for example:

        -  In the
           [entry_fulfillment][google.cloud.dialogflow.cx.v3beta1.Page.entry_fulfillment]
           of a [Page][google.cloud.dialogflow.cx.v3beta1.Page] if entering
           the page indicates that the conversation succeeded.
        -  In a webhook response when you determine that you handled the
           customer issue.

        Attributes:
            metadata (google.protobuf.struct_pb2.Struct):
                Custom metadata. Dialogflow doesn't impose
                any structure on this.
        """

        metadata = proto.Field(proto.MESSAGE, number=1, message=struct_pb2.Struct,)

    class OutputAudioText(proto.Message):
        r"""A text or ssml response that is preferentially used for TTS
        output audio synthesis, as described in the comment on the
        ResponseMessage message.

        Attributes:
            text (str):
                The raw text to be synthesized.
            ssml (str):
                The SSML text to be synthesized. For more information, see
                `SSML </speech/text-to-speech/docs/ssml>`__.
            allow_playback_interruption (bool):
                Output only. Whether the playback of this
                message can be interrupted by the end user's
                speech and the client can then starts the next
                Dialogflow request.
        """

        text = proto.Field(proto.STRING, number=1, oneof="source",)
        ssml = proto.Field(proto.STRING, number=2, oneof="source",)
        allow_playback_interruption = proto.Field(proto.BOOL, number=3,)

    class EndInteraction(proto.Message):
        r"""Indicates that interaction with the Dialogflow agent has
        ended. This message is generated by Dialogflow only and not
        supposed to be defined by the user.
            """

    class PlayAudio(proto.Message):
        r"""Specifies an audio clip to be played by the client as part of
        the response.

        Attributes:
            audio_uri (str):
                Required. URI of the audio clip. Dialogflow
                does not impose any validation on this value. It
                is specific to the client that reads it.
            allow_playback_interruption (bool):
                Output only. Whether the playback of this
                message can be interrupted by the end user's
                speech and the client can then starts the next
                Dialogflow request.
        """

        audio_uri = proto.Field(proto.STRING, number=1,)
        allow_playback_interruption = proto.Field(proto.BOOL, number=2,)

    class MixedAudio(proto.Message):
        r"""Represents an audio message that is composed of both segments
        synthesized from the Dialogflow agent prompts and ones hosted
        externally at the specified URIs. The external URIs are specified
        via
        [play_audio][google.cloud.dialogflow.cx.v3beta1.ResponseMessage.play_audio].
        This message is generated by Dialogflow only and not supposed to be
        defined by the user.

        Attributes:
            segments (Sequence[google.cloud.dialogflowcx_v3beta1.types.ResponseMessage.MixedAudio.Segment]):
                Segments this audio response is composed of.
        """

        class Segment(proto.Message):
            r"""Represents one segment of audio.
            Attributes:
                audio (bytes):
                    Raw audio synthesized from the Dialogflow
                    agent's response using the output config
                    specified in the request.
                uri (str):
                    Client-specific URI that points to an audio
                    clip accessible to the client. Dialogflow does
                    not impose any validation on it.
                allow_playback_interruption (bool):
                    Output only. Whether the playback of this
                    segment can be interrupted by the end user's
                    speech and the client should then start the next
                    Dialogflow request.
            """

            audio = proto.Field(proto.BYTES, number=1, oneof="content",)
            uri = proto.Field(proto.STRING, number=2, oneof="content",)
            allow_playback_interruption = proto.Field(proto.BOOL, number=3,)

        segments = proto.RepeatedField(
            proto.MESSAGE, number=1, message="ResponseMessage.MixedAudio.Segment",
        )

    text = proto.Field(proto.MESSAGE, number=1, oneof="message", message=Text,)
    payload = proto.Field(
        proto.MESSAGE, number=2, oneof="message", message=struct_pb2.Struct,
    )
    conversation_success = proto.Field(
        proto.MESSAGE, number=9, oneof="message", message=ConversationSuccess,
    )
    output_audio_text = proto.Field(
        proto.MESSAGE, number=8, oneof="message", message=OutputAudioText,
    )
    live_agent_handoff = proto.Field(
        proto.MESSAGE, number=10, oneof="message", message=LiveAgentHandoff,
    )
    end_interaction = proto.Field(
        proto.MESSAGE, number=11, oneof="message", message=EndInteraction,
    )
    play_audio = proto.Field(
        proto.MESSAGE, number=12, oneof="message", message=PlayAudio,
    )
    mixed_audio = proto.Field(
        proto.MESSAGE, number=13, oneof="message", message=MixedAudio,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
