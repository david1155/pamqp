# -*- encoding: utf-8 -*-
import datetime
import unittest

from pamqp import body, commands, frame, header


class DemarshalingTests(unittest.TestCase):
    def test_protocol_header(self):
        # Decode the frame and validate lengths
        frame_data = b'AMQP\x00\x00\t\x01'
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 8,
            'Bytes consumed did not match expectation: %i, %i' % (consumed, 8))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'ProtocolHeader',
                         ('Frame was of wrong type, expected ProtocolHeader, '
                          'received %s' % frame_obj.name))

        self.assertEqual((frame_obj.major_version, frame_obj.minor_version,
                          frame_obj.revision), (0, 9, 1),
                         'Protocol version is incorrect')

    def test_heartbeat(self):
        frame_data = b'\x08\x00\x00\x00\x00\x00\x00\xce'
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 8,
            'Bytes consumed did not match expectation: %i, %i' % (consumed, 8))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(frame_obj.name, 'Heartbeat',
                         ('Frame was of wrong type, expected Heartbeat, '
                          'received %s' % frame_obj.name))

    def test_basic_ack(self):
        expectation = {'multiple': False, 'delivery_tag': 1}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00\x00'
            b'\x00\x00\x00\x01\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 21, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 21))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Ack',
            f'Frame was of wrong type, expected Basic.Ack, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_cancel(self):
        expectation = {'consumer_tag': 'ctag1.0', 'nowait': False}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07ctag1.0\x00' b'\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 21, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 21))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Cancel',
            f'Frame was of wrong type, expected Basic.Cancel, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_cancelok(self):
        expectation = {'consumer_tag': 'ctag1.0'}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07ctag1.0' b'\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.CancelOk',
            f'Frame was of wrong type, expected Basic.CancelOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_consume(self):
        expectation = {
            'exclusive': False,
            'nowait': False,
            'no_local': False,
            'consumer_tag': 'ctag1.0',
            'queue': 'test',
            'arguments': {},
            'ticket': 0,
            'no_ack': False
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x18\x00<\x00\x14\x00\x00\x04'
            b'test\x07ctag1.0\x00\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 32, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 32))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Consume',
            f'Frame was of wrong type, expected Basic.Consume, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_consumeok(self):
        expectation = {'consumer_tag': 'ctag1.0'}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x15\x07ctag1.0' b'\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.ConsumeOk',
            f'Frame was of wrong type, expected Basic.ConsumeOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_deliver(self):
        expectation = {
            'consumer_tag': 'ctag1.0',
            'delivery_tag': 1,
            'redelivered': False,
            'exchange': '',
            'routing_key': 'test'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x1b\x00<\x00<\x07ctag1.0'
            b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x04test\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 35, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 35))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Deliver',
            f'Frame was of wrong type, expected Basic.Deliver, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_get(self):
        expectation = {'queue': 'test', 'ticket': 0, 'no_ack': False}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00F\x00\x00\x04' b'test\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Get',
            f'Frame was of wrong type, expected Basic.Get, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_getempty(self):
        expectation = {'cluster_id': ''}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00<\x00H\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.GetEmpty',
            f'Frame was of wrong type, expected Basic.GetEmpty, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_getok(self):
        expectation = {
            'message_count': 4614,
            'redelivered': False,
            'routing_key': 'test',
            'delivery_tag': 16,
            'exchange': ''
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x17\x00<\x00G\x00\x00\x00\x00'
            b'\x00\x00\x00\x10\x00\x00\x04test\x00\x00\x12\x06\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 31, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 31))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.GetOk',
            f'Frame was of wrong type, expected Basic.GetOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_nack(self):
        expectation = {'requeue': False, 'multiple': False, 'delivery_tag': 1}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\r\x00<\x00x\x00\x00\x00\x00'
            b'\x00\x00\x00\x01\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 21, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 21))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Nack',
            f'Frame was of wrong type, expected Basic.Nack, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_content_header(self):
        result = frame.unmarshal(frame.marshal(header.ContentHeader(0, 100),
                                               1))
        self.assertEqual(result[2].body_size, 100)

    def test_content_body(self):
        result = frame.unmarshal(frame.marshal(body.ContentBody(b'TEST'), 1))
        self.assertEqual(len(result[2]), 4)

    def test_basic_properties(self):
        encoded_properties = (b'\xff\xfc\x10application/json\x04gzip\x00\x00'
                              b'\x00\x1d\x03bazS\x00\x00\x00\x08Test \xe2\x9c'
                              b'\x88\x03fooS\x00\x00\x00\x03bar\x01\x00$a5304'
                              b'5ef-f174-4621-9ff2-ac0b8fbe6e4a\x12unmarshali'
                              b'ng_tests\n1345274026$746a1902-39dc-47cf-9471-'
                              b'9feecda35660\x00\x00\x00\x00Pj\xb9\x07\x08uni'
                              b'ttest\x04pika\x18frame_unmarshaling_tests\x00')
        properties = {
            'content_type': 'application/json',
            'content_encoding': 'gzip',
            'headers': {
                'foo': 'bar',
                'baz': 'Test ✈'
            },
            'delivery_mode': 1,
            'priority': 0,
            'correlation_id': 'a53045ef-f174-4621-9ff2-ac0b8fbe6e4a',
            'reply_to': 'unmarshaling_tests',
            'expiration': '1345274026',
            'message_id': '746a1902-39dc-47cf-9471-9feecda35660',
            'timestamp': datetime.datetime(2012, 10, 2, 9, 51, 3),
            'message_type': 'unittest',
            'user_id': 'pika',
            'app_id': 'frame_unmarshaling_tests',
            'cluster_id': ''
        }

        obj = header.ContentHeader()
        offset, flags = obj._get_flags(encoded_properties)

        # Decode the frame and validate lengths
        obj = commands.Basic.Properties()
        obj.unmarshal(flags, encoded_properties[offset:])

        for key in properties:
            self.assertEqual(
                getattr(obj, key), properties[key],
                '%r value of %r did not match expectation of %r' %
                (key, getattr(obj, key), properties[key]))

    def test_basic_publish(self):
        expectation = {
            'ticket': 0,
            'mandatory': False,
            'routing_key': 'test',
            'immediate': False,
            'exchange': ''
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\r\x00<\x00(\x00\x00\x00' b'\x04test\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 21, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 21))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Publish',
            f'Frame was of wrong type, expected Basic.Publish, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_qos(self):
        expectation = {
            'prefetch_count': 1,
            'prefetch_size': 0,
            'global_': False
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x0b\x00<\x00\n\x00\x00\x00'
            b'\x00\x00\x01\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 19, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 19))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Qos',
            f'Frame was of wrong type, expected Basic.Qos, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_qosok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00<\x00\x0b\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.QosOk',
            f'Frame was of wrong type, expected Basic.QosOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_recover(self):
        expectation = {'requeue': False}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00<\x00n\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Recover',
            f'Frame was of wrong type, expected Basic.Recover, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_recoverasync(self):
        expectation = {'requeue': False}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00<\x00d\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)
        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.RecoverAsync',
            f'Frame was of wrong type, expected Basic.RecoverAsync, received {frame_obj.name}',
        )

        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_recoverok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00<\x00o\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.RecoverOk',
            f'Frame was of wrong type, expected Basic.RecoverOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_reject(self):
        expectation = {'requeue': True, 'delivery_tag': 16}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\r\x00<\x00Z\x00\x00\x00\x00'
            b'\x00\x00\x00\x10\x01\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 21, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 21))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Reject',
            f'Frame was of wrong type, expected Basic.Reject, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_basic_return(self):
        expectation = {
            'reply_code': 200,
            'reply_text': 'Normal shutdown',
            'routing_key': 'foo.bar',
            'exchange': 'foo'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00"\x00<\x002\x00\xc8\x0f'
            b'Normal shutdown\x03foo\x07foo.bar\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 42, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 42))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Basic.Return',
            f'Frame was of wrong type, expected Basic.Return, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_close(self):
        expectation = {
            'class_id': 0,
            'method_id': 0,
            'reply_code': 200,
            'reply_text': 'Normal shutdown'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x1a\x00\x14\x00(\x00\xc8\x0f'
            b'Normal shutdown\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 34, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 34))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.Close',
            f'Frame was of wrong type, expected Channel.Close, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_closeok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00\x14\x00)\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.CloseOk',
            f'Frame was of wrong type, expected Channel.CloseOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_flow(self):
        expectation = {'active': True}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\x14\x01\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.Flow',
            f'Frame was of wrong type, expected Channel.Flow, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_flowok(self):
        expectation = {'active': True}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\x15\x01\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.FlowOk',
            f'Frame was of wrong type, expected Channel.FlowOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_open(self):
        expectation = {'out_of_band': ''}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\n\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.Open',
            f'Frame was of wrong type, expected Channel.Open, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_channel_openok(self):
        expectation = {'channel_id': ''}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x08\x00\x14\x00\x0b\x00\x00' b'\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed,
            16,
            f'Bytes consumed did not match expectation: {consumed}, 16',
        )

        self.assertEqual(
            channel, 1, f'Channel number did not match expectation: {channel}, 1'
        )

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Channel.OpenOk',
            f'Frame was of wrong type, expected Channel.OpenOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_confirm_select(self):
        expectation = {'nowait': False}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x05\x00U\x00\n\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Confirm.Select',
            f'Frame was of wrong type, expected Confirm.Select, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_confirm_selectok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00U\x00\x0b\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Confirm.SelectOk',
            f'Frame was of wrong type, expected Confirm.SelectOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_close(self):
        expectation = {
            'class_id': 0,
            'method_id': 0,
            'reply_code': 200,
            'reply_text': 'Normal shutdown'
        }

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x1a\x00\n\x002\x00\xc8\x0f'
            b'Normal shutdown\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 34, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 34))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.Close',
            f'Frame was of wrong type, expected Connection.Close, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_closeok(self):
        expectation = {}

        frame_data = b'\x01\x00\x00\x00\x00\x00\x04\x00\n\x003\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.CloseOk',
            f'Frame was of wrong type, expected Connection.CloseOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_open(self):
        expectation = {'insist': True, 'capabilities': '', 'virtual_host': '/'}

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x08\x00\n\x00(\x01/\x00' b'\x01\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 16, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 16))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.Open',
            f'Frame was of wrong type, expected Connection.Open, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_openok(self):
        expectation = {'known_hosts': ''}

        frame_data = b'\x01\x00\x00\x00\x00\x00\x05\x00\n\x00)\x00\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 13, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 13))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.OpenOk',
            f'Frame was of wrong type, expected Connection.OpenOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_secure(self):
        expectation = {'challenge': ''}

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x08\x00\n\x00\x14\x00\x00' b'\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 16, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 16))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.Secure',
            f'Frame was of wrong type, expected Connection.Secure, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_secureok(self):
        expectation = {'response': ''}

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x08\x00\n\x00\x15\x00\x00' b'\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 16, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 16))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.SecureOk',
            f'Frame was of wrong type, expected Connection.SecureOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_start(self):
        expectation = {
            'server_properties': {
                'information': (
                    'Licensed under the MPL.  See http://www.rabbitmq.com/'),
                'product': 'RabbitMQ',
                'copyright': 'Copyright (C) 2007-2011 VMware, Inc.',
                'capabilities': {
                    'exchange_exchange_bindings': True,
                    'consumer_cancel_notify': True,
                    'publisher_confirms': True,
                    'basic.nack': True
                },
                'platform': 'Erlang/OTP',
                'version': '2.6.1'
            },
            'version_minor': 9,
            'mechanisms': 'PLAIN AMQPLAIN',
            'locales': 'en_US',
            'version_major': 0
        }

        frame_data = (
            b'\x01\x00\x00\x00\x00\x01G\x00\n\x00\n\x00\t'
            b'\x00\x00\x01"\x0ccapabilitiesF\x00\x00\x00X'
            b'\x12publisher_confirmst\x01\x1aexchange_exc'
            b'hange_bindingst\x01\nbasic.nackt\x01\x16con'
            b'sumer_cancel_notifyt\x01\tcopyrightS\x00'
            b'\x00\x00$Copyright (C) 2007-2011 VMware, I'
            b'nc.\x0binformationS\x00\x00\x005Licensed u'
            b'nder the MPL.  See http://www.rabbitmq.com'
            b'/\x08platformS\x00\x00\x00\nErlang/OTP\x07'
            b'productS\x00\x00\x00\x08RabbitMQ\x07versio'
            b'nS\x00\x00\x00\x052.6.1\x00\x00\x00\x0ePLA'
            b'IN AMQPLAIN\x00\x00\x00\x05en_US\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 335, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 335))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.Start',
            f'Frame was of wrong type, expected Connection.Start, received {frame_obj.name}',
        )
        self.maxDiff = 32768

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_startok(self):
        expectation = {
            'locale': 'en_US',
            'mechanism': 'PLAIN',
            'client_properties': {
                'platform': 'Python 2.7.1',
                'product': 'Pika Python Client Library',
                'version': '0.9.6-pre0',
                'capabilities': {
                    'consumer_cancel_notify': True,
                    'publisher_confirms': True,
                    'basic.nack': True
                },
                'information': 'See http://pika.github.com'
            },
            'response': '\x00guest\x00guest'
        }

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\xf4\x00\n\x00\x0b'
            b'\x00\x00\x00\xd0\x08platformS\x00\x00\x00'
            b'\x0cPython 2.7.1\x07productS\x00\x00\x00'
            b'\x1aPika Python Client Library\x07versionS'
            b'\x00\x00\x00\n0.9.6-pre0\x0ccapabilitiesF'
            b'\x00\x00\x00;\x16consumer_cancel_notifyt'
            b'\x01\x12publisher_confirmst\x01\nbasic.nack'
            b't\x01\x0binformationS\x00\x00\x00\x1aSee '
            b'http://pika.github.com\x05PLAIN\x00\x00'
            b'\x00\x0c\x00guest\x00guest\x05en_US\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 252, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 252))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.StartOk',
            f'Frame was of wrong type, expected Connection.StartOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_tune(self):
        expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1e\x00\x00'
            b'\x00\x02\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.Tune',
            f'Frame was of wrong type, expected Connection.Tune, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_connection_tuneok(self):
        expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

        frame_data = (
            b'\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1f\x00\x00'
            b'\x00\x02\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Connection.TuneOk',
            f'Frame was of wrong type, expected Connection.TuneOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_content_body_frame(self):
        frame_data = (b'\x03\x00\x00\x00\x00\x00"Hello World #0:1316899165.'
                      b'75516605\xce')

        expectation = b'Hello World #0:1316899165.75516605'

        # Decode the frame and validate lengths
        consumed, channel, data = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 42, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 42))

        self.assertEqual(
            channel, 0,
            'Channel number did not match expectation: %i, %i' % (channel, 0))

        # Validate the unmarshaled data matches the expectation
        self.assertEqual(data.value, expectation)

    def test_exchange_bind(self):
        expectation = {
            'arguments': {},
            'source': '',
            'ticket': 0,
            'destination': '',
            'nowait': False,
            'routing_key': 'foo.bar'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x15\x00(\x00\x1e\x00\x00'
            b'\x00\x00\x07foo.bar\x00\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 29, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 29))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.Bind',
            f'Frame was of wrong type, expected Exchange.Bind, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_bindok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x1f\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.BindOk',
            f'Frame was of wrong type, expected Exchange.BindOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_declare(self):
        expectation = {
            'nowait': False,
            'exchange': 'pika_test_exchange',
            'durable': False,
            'passive': False,
            'internal': False,
            'arguments': {},
            'ticket': 0,
            'exchange_type': 'direct',
            'auto_delete': False
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00%\x00(\x00\n\x00\x00\x12pika_'
            b'test_exchange\x06direct\x00\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 45, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 45))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.Declare',
            f'Frame was of wrong type, expected Exchange.Declare, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_declareok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x0b\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.DeclareOk',
            f'Frame was of wrong type, expected Exchange.DeclareOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_delete(self):
        expectation = {
            'ticket': 0,
            'if_unused': False,
            'nowait': False,
            'exchange': 'pika_test_exchange'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x1a\x00(\x00\x14\x00\x00\x12'
            b'pika_test_exchange\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 34, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 34))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.Delete',
            f'Frame was of wrong type, expected Exchange.Delete, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_deleteok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x15\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.DeleteOk',
            f'Frame was of wrong type, expected Exchange.DeleteOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_unbind(self):
        expectation = {
            'arguments': {},
            'source': '',
            'ticket': 0,
            'destination': '',
            'nowait': False,
            'routing_key': 'foo.bar'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x15\x00(\x00(\x00\x00\x00'
            b'\x00\x07foo.bar\x00\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 29, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 29))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.Unbind',
            f'Frame was of wrong type, expected Exchange.Unbind, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_exchange_unbindok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00(\x003\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Exchange.UnbindOk',
            f'Frame was of wrong type, expected Exchange.UnbindOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_bind(self):
        expectation = {
            'nowait': False,
            'exchange': 'pika_test_exchange',
            'routing_key': 'test_routing_key',
            'queue': 'pika_test_queue',
            'arguments': {},
            'ticket': 0
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00?\x002\x00\x14\x00'
            b'\x00\x0fpika_test_queue\x12pika_test_excha'
            b'nge\x10test_routing_key\x00\x00\x00\x00\x00'
            b'\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 71, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 71))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.Bind',
            f'Frame was of wrong type, expected Queue.Bind, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_bindok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x002\x00\x15\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.BindOk',
            f'Frame was of wrong type, expected Queue.BindOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_declare(self):
        expectation = {
            'passive': False,
            'nowait': False,
            'exclusive': False,
            'durable': True,
            'queue': 'test',
            'arguments': {},
            'ticket': 0,
            'auto_delete': False
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x10\x002\x00\n\x00\x00\x04'
            b'test\x02\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 24, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 24))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.Declare',
            f'Frame was of wrong type, expected Queue.Declare, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_declareok(self):
        expectation = {
            'queue': 'test',
            'message_count': 4615,
            'consumer_count': 0
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x11\x002\x00\x0b\x04test'
            b'\x00\x00\x12\x07\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 25, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 25))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.DeclareOk',
            f'Frame was of wrong type, expected Queue.DeclareOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_delete(self):
        expectation = {
            'queue': 'pika_test_queue',
            'ticket': 0,
            'if_empty': False,
            'nowait': False,
            'if_unused': False
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x17\x002\x00(\x00\x00\x0f'
            b'pika_test_queue\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 31, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 31))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.Delete',
            f'Frame was of wrong type, expected Queue.Delete, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_deleteok(self):
        expectation = {'message_count': 0}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x08\x002\x00)\x00\x00\x00' b'\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 16, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 16))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.DeleteOk',
            f'Frame was of wrong type, expected Queue.DeleteOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_purge(self):
        expectation = {'queue': 'test', 'ticket': 0, 'nowait': False}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x0c\x002\x00\x1e\x00\x00'
            b'\x04test\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 20, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 20))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.Purge',
            f'Frame was of wrong type, expected Queue.Purge, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_purgeok(self):
        expectation = {'message_count': 1}

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00\x08\x002\x00\x1f\x00\x00\x00' b'\x01\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 16, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 16))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.PurgeOk',
            f'Frame was of wrong type, expected Queue.PurgeOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_unbind(self):
        expectation = {
            'queue': 'pika_test_queue',
            'arguments': {},
            'ticket': 0,
            'routing_key': 'test_routing_key',
            'exchange': 'pika_test_exchange'
        }

        frame_data = (
            b'\x01\x00\x01\x00\x00\x00>\x002\x002\x00\x00\x0f'
            b'pika_test_queue\x12pika_test_exchange\x10test_routing'
            b'_key\x00\x00\x00\x00\xce'
        )
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 70, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 70))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.Unbind',
            f'Frame was of wrong type, expected Queue.Unbind, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_queue_unbindok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x002\x003\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Queue.UnbindOk',
            f'Frame was of wrong type, expected Queue.UnbindOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_commit(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x14\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.Commit',
            f'Frame was of wrong type, expected Tx.Commit, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_commitok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x15\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.CommitOk',
            f'Frame was of wrong type, expected Tx.CommitOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_rollback(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x1e\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.Rollback',
            f'Frame was of wrong type, expected Tx.Rollback, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_rollbackok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x1f\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.RollbackOk',
            f'Frame was of wrong type, expected Tx.RollbackOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_select(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\n\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.Select',
            f'Frame was of wrong type, expected Tx.Select, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_tx_selectok(self):
        expectation = {}

        frame_data = b'\x01\x00\x01\x00\x00\x00\x04\x00Z\x00\x0b\xce'
        # Decode the frame and validate lengths
        consumed, channel, frame_obj = frame.unmarshal(frame_data)

        self.assertEqual(
            consumed, 12, 'Bytes consumed did not match expectation: %i, %i' %
            (consumed, 12))

        self.assertEqual(
            channel, 1,
            'Channel number did not match expectation: %i, %i' % (channel, 1))

        # Validate the frame name
        self.assertEqual(
            frame_obj.name,
            'Tx.SelectOk',
            f'Frame was of wrong type, expected Tx.SelectOk, received {frame_obj.name}',
        )

        # Validate the unmarshaled data matches the expectation
        self.assertDictEqual(dict(frame_obj), expectation)

    def test_properties(self):
        props = commands.Basic.Properties(
            app_id='unittest',
            content_type='application/json',
            content_encoding='bzip2',
            correlation_id='d146482a-42dd-4b8b-a620-63d62ef686f3',
            delivery_mode=2,
            expiration='100',
            headers={'foo': 'Test ✈'},
            message_id='4b5baed7-66e3-49da-bfe4-20a9651e0db4',
            message_type='foo',
            priority=10,
            reply_to='q1',
            timestamp=datetime.datetime(2019, 12, 19, 23, 29, 00))
        ch = frame.marshal(header.ContentHeader(0, 10, props), 1)
        rt_props = frame.unmarshal(ch)[2].properties
        self.assertEqual(rt_props, props)
