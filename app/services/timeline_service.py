from app.db.models.ticket_event import TicketEvent
from app.db.models.comment import Comment
from app.schemas.timeline import TimelineItem
from sqlalchemy.orm import Session


def get_ticket_timeline(db: Session, ticket_id: int):
    events = (
        db.query(TicketEvent)
        .filter(TicketEvent.ticket_id == ticket_id)
        .all()
    )

    comments = (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .all()
    )

    timeline = []

    for event in events:
        timeline.append(
            TimelineItem(
                type="event",
                event_type=event.event_type,
                from_status=event.from_status,
                to_status=event.to_status,
                user_id=event.user_id,
                created_at=event.created_at,
            )
        )

    for comment in comments:
        timeline.append(
            TimelineItem(
                type="comment",
                content=comment.content,
                user_id=comment.user_id,
                created_at=comment.created_at,
            )
        )

    # Ordenar tudo por data
    timeline.sort(key=lambda x: x.created_at)

    return timeline
