package database

import com.google.inject.Inject
import database.table.UserTable
import model.User
import slick.ast.BaseTypedType
import slick.basic.DatabaseConfig
import slick.jdbc.PostgresProfile

import scala.concurrent.ExecutionContext

class UserRepository @Inject()(
    override val driver: PostgresProfile,
    override val dbConfig: DatabaseConfig[PostgresProfile]
)(override implicit val ec: ExecutionContext)
    extends BaseRepository[User, Long](driver, dbConfig) {

  import driver.api._

  type TableType = UserTable

  override def pkType = implicitly[BaseTypedType[Long]]
  override def tableQuery = UserTable.users
}
