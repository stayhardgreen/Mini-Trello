from graphene import ObjectType, InputObjectType, String, Int, Schema, Field, Mutation, JSONString, List
import boto3
import uuid

CARDS_TABLE = 'cards'
SECTIONS_TABLE = 'sections'
access_key_id = 'AKIAYBNJI4EPU7RHB3U3'
secret_access_key = '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'
region_name = "eu-north-1"


def getItemFromCards(tableName, id, param=None):
    # Code to get the item into dynamo db
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    response = table.get_item(Key={'id': id})
    print(response['Item'])
    result = response['Item']
    if param:
        result = response['Item'][param]
    print(result)
    return result


def getItemFromSections(tableName, id, param=None):
    # Code to get the item into dynamo db
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    response = table.get_item(Key={'id': id})
    print(response['Item'])
    result = response['Item']
    if param:
        result = response['Item'][param]
    print(result)
    return result


def getAllItemsFromCards(tableName):
    results = []
    lastEvaluatedKey = None

    client = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    ).client('dynamodb', region_name=region_name)

    while True:
        if lastEvaluatedKey:
            response = client.scan(
                TableName=tableName,
                ExclusiveStartKey=lastEvaluatedKey
            )
        else:
            response = client.scan(TableName=tableName)
        lastEvaluatedKey = response.get('LastEvaluatedKey')
        results.extend(response['Items'])
        if not lastEvaluatedKey:
            break
    return results


def getAllItemsFromSections(tableName):
    results = []
    lastEvaluatedKey = None

    client = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    ).client('dynamodb', region_name=region_name)

    while True:
        if lastEvaluatedKey:
            response = client.scan(
                TableName=tableName,
                ExclusiveStartKey=lastEvaluatedKey
            )
        else:
            response = client.scan(TableName=tableName)
        lastEvaluatedKey = response.get('LastEvaluatedKey')
        results.extend(response['Items'])
        if not lastEvaluatedKey:
            break
    return results


class CardParamsInput(InputObjectType):
    id = String()
    title = String(required=True)
    label = String(required=True)
    pos = Int(required=True)
    sectionId = String(required=True)


class UpdateCardParamsInput(InputObjectType):
    id = String()
    title = String()
    label = String()
    pos = Int()
    sectionId = String()


class SectionParamsInput(InputObjectType):
    id = String()
    title = String(required=True)
    label = String(required=True)
    pos = Int(required=True)


class UpdateSectionParamsInput(InputObjectType):
    id = String()
    title = String()
    label = String()
    pos = Int()


class Card(ObjectType):
    class Meta:
        description = 'Card Parameters'
    id = String()
    title = String()
    label = String()
    pos = Int()
    sectionId = String()
    cardInfo = JSONString()


class Section(ObjectType):
    class Meta:
        description = 'Section Parameters'
    id = String()
    title = String()
    label = String()
    pos = Int()
    cards = List(lambda: Card)
    sectionInfo = JSONString()

    def resolve_cards(parent, info):
        # Query the cards associated with the section using the section's ID
        section_id = parent['id']
        cards = getAllItemsFromCards(CARDS_TABLE)
        section_cards = [
            card for card in cards if card['sectionId'] == section_id]
        return section_cards


class CreateCardEntry(Mutation):
    class Arguments:
        cardEntry = CardParamsInput(required=True)

    Output = Card

    def mutate(self, info, cardEntry):
        # Code to add the item into dynamo db
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(CARDS_TABLE)
        cardEntry['id'] = str(uuid.uuid4())
        table.put_item(Item=cardEntry)
        return Card(
            id=cardEntry.id,
            title=cardEntry.title,
            label=cardEntry.label,
            pos=cardEntry.pos,
            sectionId=cardEntry.sectionId
        )


class CreateSectionEntry(Mutation):
    class Arguments:
        sectionEntry = SectionParamsInput(required=True)

    Output = Section

    def mutate(self, info, sectionEntry):
        # Code to add the item into dynamo db
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(SECTIONS_TABLE)
        sectionEntry['id'] = str(uuid.uuid4())
        table.put_item(Item=sectionEntry)
        return Section(
            id=sectionEntry.id,
            title=sectionEntry.title,
            label=sectionEntry.label,
            pos=sectionEntry.pos,
        )


class UpdateSectionEntry(Mutation):
    class Arguments:
        sectionEntry = UpdateSectionParamsInput(required=True)

    Output = Section

    def mutate(self, info, sectionEntry):
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).client('dynamodb', region_name=region_name)
        response = dynamodb.update_item(
            TableName=SECTIONS_TABLE,
            Key={'id': {'S': sectionEntry.id}},
            UpdateExpression='SET title = :title, label = :label, pos = :pos',
            ExpressionAttributeValues={
                ':title': {'S': sectionEntry.title},
                ':label': {'S': sectionEntry.label},
                ':pos': {'N': str(sectionEntry.pos)}
            },
            ReturnValues='ALL_NEW'
        )

        if 'Attributes' in response:
            result = response['Attributes']
            return result
        else:
            raise Exception('Failed to update sections')


class UpdateCardEntry(Mutation):
    class Arguments:
        cardEntry = UpdateCardParamsInput(required=True)

    Output = Card

    def mutate(self, info, cardEntry):
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).client('dynamodb', region_name=region_name)
        response = dynamodb.update_item(
            TableName=CARDS_TABLE,
            Key={'id': {'S': cardEntry.id}},
            UpdateExpression='SET title = :title, label = :label, pos = :pos, sectionId = :sectionId',
            ExpressionAttributeValues={
                ':title': {'S': cardEntry.title},
                ':label': {'S': cardEntry.label},
                ':pos': {'N': str(cardEntry.pos)},
                ':sectionId': {'S': cardEntry.sectionId}
            },
            ReturnValues='ALL_NEW'
        )

        if 'Attributes' in response:
            result = response['Attributes']
            return result
        else:
            raise Exception('Failed to update cards')


class DeleteSectionMutation(Mutation):
    class Arguments:
        sectionEntry = UpdateSectionParamsInput(required=True)

    Output = Section

    def mutate(self, info, sectionEntry):
        # Code to delete a section from DynamoDB
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(SECTIONS_TABLE)
        cards_table = dynamodb.Table(CARDS_TABLE)
        matched_cards = Section.resolve_cards({'id': {'S': sectionEntry.id}}, info)
        for item in matched_cards:
            cards_table.delete_item(Key={'id': item['id']['S']})
        response = table.delete_item(
            Key={'id': sectionEntry.id},
            ReturnValues='ALL_OLD'
        )
        deleted_section = response.get('Attributes', None)
        return deleted_section


class DeleteCardMutation(Mutation):
    class Arguments:
        cardEntry = UpdateSectionParamsInput(required=True)

    Output = Card

    def mutate(self, info, cardEntry):
        # Code to delete a section from DynamoDB
        dynamodb = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        ).resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(CARDS_TABLE)
        response = table.delete_item(
            Key={'id': cardEntry.id},
            ReturnValues='ALL_OLD'
        )
        deleted_card = response.get('Attributes', None)
        return deleted_card


class Mutation(ObjectType):
    cardData = CreateCardEntry.Field()
    sectionData = CreateSectionEntry.Field()
    updateSectionData = UpdateSectionEntry.Field()
    updateCardData = UpdateCardEntry.Field()
    deleteSectionItem = DeleteSectionMutation.Field()
    deleteCardItem = DeleteCardMutation.Field()


class Query(ObjectType):

    cardDetails = Field(Card, cardId=Int(required=True))
    allCardData = Field(Card)

    sectionDetails = Field(Section, sectionId=Int(required=True))
    allSectionData = Field(Section)

    def resolve_allCardData(root, info):
        # Query the dynamodb here and get all the records for display
        data = {}
        data['cardInfo'] = getAllItemsFromCards(CARDS_TABLE)
        return data

    def resolve_cardDetails(root, info, cardId):
        data = {}
        data = getItemFromCards(CARDS_TABLE, cardId)
        return data

    def resolve_allSectionData(root, info):
        # Query the dynamodb here and get all the records for display
        data = {}
        data['sectionInfo'] = getAllItemsFromSections(SECTIONS_TABLE)
        print(getAllItemsFromSections(SECTIONS_TABLE))
        for section in data['sectionInfo']:
            section['cards'] = Section.resolve_cards(section, info)
        return data

    def resolve_sectionDetails(root, info, sectionId):
        data = {}
        data = getItemFromSections(SECTIONS_TABLE, sectionId)
        return data


schema = Schema(query=Query, mutation=Mutation)
