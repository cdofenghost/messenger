from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import NoResultFound, IntegrityError

from .exceptions import  ( 
    ParticipantNotFoundError, ParticipantAlreadyExistsError, 
    ChatNotFoundError, UserNotFoundError, AppError,
)
from ..schemas.participant import ParticipantCreateSchema, ParticipantSchema, ParticipationSchema
from ..models.participant import Participant

class ParticipantRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_participant(self, data: ParticipantCreateSchema) -> Participant:
        return Participant(user_id=data.user_id, chat_id=data.chat_id)
    
    def __to_participant_schema(self, participant: Participant):
        return ParticipantSchema(id=participant.id, user_id=participant.user_id, chat_id=participant.chat_id)

    def add_participant(self, create_schema: ParticipantCreateSchema) -> ParticipantSchema:
        participant = self.__to_participant(create_schema) 

        self.db.add(participant)
        self.db.commit()

        return self.__to_participant_schema(participant)

    def find_participant(self, id: int) -> ParticipantSchema:
        participant = self.db.query(Participant).filter(Participant.id == id).first()

        if participant is None:
            raise NoResultFound()
        
        return self.__to_participant_schema(participant)
    
    def find_participation(self, user_id: int, chat_id: int) -> ParticipantSchema:
        participation = self.db.query(Participant).filter(Participant.user_id == user_id,
                                                          Participant.chat_id == chat_id)
        
        if participation is None:
            raise NoResultFound()
        
        return self.__to_participant_schema(participation)
    
    def find_chat_participants(self, chat_id: int) -> list[ParticipantSchema]:
        participants = self.db.query(Participant).filter(Participant.chat_id == chat_id)

        if participants is None or participants.count() == 0:
            raise NoResultFound()
        
        return [self.__to_participant_schema(participant) 
                for participant in participants]
    
    def find_user_participations(self, user_id: int) -> list[ParticipantSchema]:
        participations = self.db.query(Participant).filter(Participant.user_id == user_id)

        if participations is None or participations.count() == 0:
            raise NoResultFound()

        return [self.__to_participant_schema(participation)
                for participation in participations]
    
    def delete_participant(self, id: int) -> ParticipantSchema:
        participant = self.db.query(Participant).filter(Participant.id == id).first()

        if participant is None:
            raise NoResultFound()

        self.db.delete(participant)
        self.db.commit()

        return self.__to_participant_schema(participant)
    
    def delete_participation(self, participation_schema: ParticipationSchema) -> ParticipantSchema:
        participation = self.db.query(Participant).filter(Participant.user_id == participation_schema.user_id,
                                                          Participant.chat_id == participation_schema.chat_id).first()

        if participation is None:
            raise NoResultFound()
        
        self.db.delete(participation)
        self.db.commit()

        return self.__to_participant_schema(participation)
    

class ParticipantService:
    def __init__(self, repository: ParticipantRepository):
        self.repository = repository

    def add_participant(self, participation_data: ParticipantCreateSchema) -> ParticipantSchema:
        try:
            return self.repository.add_participant(participation_data)
        except IntegrityError as e:
            error_message = str(e).lower()

            if "foreign key constraint" in error_message:
                if "user_id" in error_message:
                    raise UserNotFoundError()
                elif "chat_id" in error_message:
                    raise ChatNotFoundError()
                else:
                    raise AppError(str(e))

            elif "unique constraint" in error_message:
                raise ParticipantAlreadyExistsError()

            else:
                raise AppError(str(e))
            

    def get_chat_participants(self, chat_id: int) -> list[ParticipantSchema]:
        try:
            return self.repository.find_chat_participants(chat_id)
        except NoResultFound:
            raise ParticipantNotFoundError(f"Chat with id = {chat_id} doesn't exist or has no participants.")
        
    def get_participant(self, id: int) -> ParticipantSchema:
        try:
            return self.repository.find_participant(id)
        except NoResultFound:
            raise ParticipantNotFoundError()

    def remove_participant(self, id: int) -> ParticipantSchema:
        try:
            return self.repository.delete_participant(id)
        except NoResultFound:
            raise ParticipantNotFoundError()
        

    def get_user_participations(self, user_id: int) -> list[ParticipantSchema]:
        try:
            return self.repository.find_user_participations(user_id)
        except NoResultFound:
            raise ParticipantNotFoundError("User isn't currently participating in any of the chats.")
    
    def get_participation(self, user_id: int, chat_id: int) -> ParticipantSchema:
        try:
            return self.repository.find_participation(user_id, chat_id)
        except NoResultFound:
            raise ParticipantNotFoundError()
        
    def remove_participation(self, participation: ParticipationSchema) -> ParticipantSchema:
        try:
            return self.repository.delete_participation(participation)
        except NoResultFound:
            raise ParticipantNotFoundError()