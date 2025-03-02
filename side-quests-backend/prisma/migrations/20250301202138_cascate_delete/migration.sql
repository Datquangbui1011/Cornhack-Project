-- DropForeignKey
ALTER TABLE "Project" DROP CONSTRAINT "Project_categoryId_fkey";

-- DropForeignKey
ALTER TABLE "StepBreakdown" DROP CONSTRAINT "StepBreakdown_stepsId_fkey";

-- DropForeignKey
ALTER TABLE "StepsCompleted" DROP CONSTRAINT "StepsCompleted_stepsId_fkey";

-- DropForeignKey
ALTER TABLE "StepsCompleted" DROP CONSTRAINT "StepsCompleted_userProjectId_fkey";

-- DropForeignKey
ALTER TABLE "UserProject" DROP CONSTRAINT "UserProject_projectId_fkey";

-- AddForeignKey
ALTER TABLE "Project" ADD CONSTRAINT "Project_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UserProject" ADD CONSTRAINT "UserProject_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "Project"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StepBreakdown" ADD CONSTRAINT "StepBreakdown_stepsId_fkey" FOREIGN KEY ("stepsId") REFERENCES "Steps"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StepsCompleted" ADD CONSTRAINT "StepsCompleted_userProjectId_fkey" FOREIGN KEY ("userProjectId") REFERENCES "UserProject"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StepsCompleted" ADD CONSTRAINT "StepsCompleted_stepsId_fkey" FOREIGN KEY ("stepsId") REFERENCES "Steps"("id") ON DELETE CASCADE ON UPDATE CASCADE;
