#transferl2amount/receiverid/receiverkey/receiverpositionid
def transferl2():
        create_transfer_result = client.private.create_transfer(
                amount = transferl2amount,
                position_id = account['positionId'],
                expiration = epoch_seconds_to_iso(time.time() + 604801),
                receiver_account_id = receiverid,
                receiver_public_key = receiverkey,
                receiver_position_id = receiverpositionid,
        )
