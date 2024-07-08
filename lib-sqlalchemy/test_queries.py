import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.sql import and_, func, select

# Assuming `metadata` and `engine` are already defined
metadata = sa.MetaData()

# Define the services_meta_data table
services_meta_data = sa.Table(
    "services_meta_data",
    metadata,
    sa.Column("key", sa.String, nullable=False),
    sa.Column("version", sa.String, nullable=False),
    sa.Column(
        "owner",
        sa.BigInteger,
        sa.ForeignKey(
            "groups.gid",
            name="fk_services_meta_data_gid_groups",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=True,
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("description", sa.String, nullable=False),
    sa.Column("thumbnail", sa.String, nullable=True),
    sa.Column(
        "classifiers",
        ARRAY(sa.String, dimensions=1),
        nullable=False,
        server_default="{}",
    ),
    sa.Column("created", sa.DateTime(), nullable=False, server_default=func.now()),
    sa.Column(
        "modified",
        sa.DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    sa.Column("deprecated", sa.DateTime(), nullable=True, server_default=None),
    sa.Column("quality", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    sa.PrimaryKeyConstraint("key", "version", name="services_meta_data_pk"),
)


# Define other necessary tables
users = sa.Table("users", metadata, autoload_with=engine)
groups = sa.Table("groups", metadata, autoload_with=engine)
users_to_groups = sa.Table("users_to_groups", metadata, autoload_with=engine)

# Define the main query
def get_service(key, version):
    subquery_history = (
        select(
            services_meta_data.c.key,
            func.json_agg(
                sa.literal_column(
                    "json_build_object('version', version, 'deprecated', deprecated, 'created', created)"
                )
            ).label("history"),
        )
        .where(services_meta_data.c.key == key)
        .group_by(services_meta_data.c.key)
        .subquery()
    )

    return (
        select(
            services_meta_data.c.key,
            services_meta_data.c.version,
            services_meta_data.c.name,
            services_meta_data.c.description,
            services_meta_data.c.thumbnail,
            users.c.email.label("owner_email"),
            services_meta_data.c.classifiers,
            services_meta_data.c.quality,
            services_meta_data.c.created,
            services_meta_data.c.modified,
            services_meta_data.c.deprecated,
            subquery_history.c.history,
        )
        .select_from(services_meta_data)
        .join(groups, groups.c.gid == services_meta_data.c.owner, isouter=True)
        .join(users_to_groups, users_to_groups.c.gid == groups.c.gid, isouter=True)
        .join(users, users.c.id == users_to_groups.c.uid, isouter=True)
        .join(
            subquery_history,
            services_meta_data.c.key == subquery_history.c.key,
            isouter=True,
        )
        .where(
            and_(
                services_meta_data.c.key == key, services_meta_data.c.version == version
            )
        )
    )


# Example usage
service = get_service("simcore/services/dynamic/my-super-service", "1.0.0")
print(service)
