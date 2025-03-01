-- AlterTable
CREATE SEQUENCE category_id_seq;
ALTER TABLE "Category" ALTER COLUMN "id" SET DEFAULT nextval('category_id_seq');
ALTER SEQUENCE category_id_seq OWNED BY "Category"."id";

-- AlterTable
ALTER TABLE "Project" ALTER COLUMN "updated_at" DROP DEFAULT;

-- AlterTable
CREATE SEQUENCE userproject_id_seq;
ALTER TABLE "UserProject" ALTER COLUMN "id" SET DEFAULT nextval('userproject_id_seq');
ALTER SEQUENCE userproject_id_seq OWNED BY "UserProject"."id";
